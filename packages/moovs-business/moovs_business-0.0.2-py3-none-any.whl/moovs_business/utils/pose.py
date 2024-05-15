import json
from typing import List, Tuple

from pyqflow import (
    QAggregate,
    QBatching,
    QClassicMap,
    QRemoteMap,
    QUnBatching,
    QWorkFlow,
    QNativeMap,
    QControlledMap,
    QCallback,
    QFlatMap,
)
from pyqflow.actor import QActor
from functools import partial
from moovs_business.utils.helpers import scale_pose_predictions, extract_crops
from moovs_business.utils.serialize import arranging_pose_inputs
from moovs_business.constants import URL
from moovs_business.flows.tracking import TrackingFlow
import numpy as np
from moovs_business.utils.math import (
    track_feature_similarity,
    track_missing_similarity,
    group_tracks,
    score_tracks,
)


def calculate_similarity(track1, track2, feature_similarity_threshold=0.3):
    class1 = track1["class_id"].max()
    class2 = track2["class_id"].max()
    # track1_id = track1["track_id"]
    # track2_id = track2["track_id"]
    # check if both tracks are of the same class
    if class1 != class2:
        return 0  # not the same track

    # similarity matrix is based on:
    # if the feature_similarity is less than 0.3, then assume that it's not the same track
    # if its superior to 0.3 use the tracking missing frames:
    # ex: if a track with 100 frames is missing the first 10 frames and the other is missing the last 90 frames, is very likely the same object

    # each features used to calculate the similarity has to be normalized between 0 and 1
    # being 1 the most likely to be the same track me and 0 different tracks

    if class1 == 0:
        feat_simi = track_feature_similarity(
            track1["features"], track2["features"], metric="cosine", budget_dim=50
        )
        if feat_simi < feature_similarity_threshold:
            return 0

    return track_missing_similarity(track1["bbox"], track2["bbox"])


def merge_tracks(tracks: List):
    """This function merges a group of tracks.
    It takes the union of the bounding boxes, and the union of the keypoints coordinates.
    It takes into account when the are missing. In case of overlap ( which should be rare ), takes the most confident bounding box.
    """

    source, targets = tracks[0], tracks[1:]
    class_id = source["class_id"].max()
    source_tracked_step = source["tracked_time_step"].max()
    source_tracked_id = source["track_id"]
    # ----
    source_pos, source_score = source["bbox"], source["score"]
    # source_kp, source_kp_scores = source["keypoint_coords"], source["keypoint_scores"]
    source_missing = np.isnan(source_pos).any(axis=1)
    source_not_missing = ~source_missing

    for target in targets:
        source_tracked_id = (
            source_tracked_id
            if source_tracked_id < target["track_id"]
            else target["track_id"]
        )

        target_mvg_avg, target_pos, target_score, target_tracked_step = (
            target["mv_avg"],
            target["bbox"],
            target["score"],
            target["tracked_time_step"].max(),
        )

        target_kp, target_kp_scores = (
            target["keypoint_coords"],
            target["keypoint_scores"],
        )

        # inspect when target is not missing
        target_missing = np.isnan(target_pos).any(axis=1)
        target_not_missing = ~target_missing

        # check if minimum tracked time step
        source_tracked_step = min(target_tracked_step, source_tracked_step)

        # check frames that are easy to merge - when track1 is missing and track2 is not missing or vice versa
        easy_add = np.logical_and(
            source_missing,
            target_not_missing,
        )
        easy_add_count = easy_add.sum()

        # check frames that are ambiguous to merge - when both tracks are not missing
        ambiguous = np.logical_and(
            source_not_missing,
            target_not_missing,
        )
        ambiguous = np.expand_dims(ambiguous, axis=1)

        # when its ambiguous, take the most confident bounding box
        hard_add = np.squeeze(
            np.logical_and(ambiguous, (target_score > source_score)), axis=1
        )
        hard_add_count = hard_add.sum()

        # merge is done here
        if easy_add_count > 0:
            source["bbox"][easy_add] = target_pos[easy_add]
            source["mv_avg"][easy_add] = target_mvg_avg[easy_add]
            source["score"][easy_add] = target_score[easy_add]

        if hard_add_count > 0:
            source["mv_avg"][hard_add] = target_mvg_avg[hard_add]
            source["bbox"][hard_add] = target_pos[hard_add]
            source["score"][hard_add] = target_score[hard_add]

        if class_id == 0:
            if easy_add_count > 0:
                source["keypoint_coords"][easy_add] = target_kp[easy_add]
                source["keypoint_scores"][easy_add] = target_kp_scores[easy_add]
            if hard_add_count > 0:
                source["keypoint_coords"][hard_add] = target_kp[hard_add]
                source["keypoint_scores"][hard_add] = target_kp_scores[hard_add]

    final_source_missing = np.isnan(source["bbox"]).any(axis=1)

    source["tracked_time_step"] = source_tracked_step
    source["track_id"] = source_tracked_id
    return source


def group_merge_filter_and_sort_tracks(
    tracks,
    threshold=0.05,
    valid_classes=[0, 32],
    single_class=False,
    class_dependent=False,
):
    """
    This functions groups tracks based on similiarity.
    Given a similarity matrix it decides if it should merge tracks.
    Finally, the tracks are sorted with order of importance.
    """
    # remove any track that does not have its class in valid_classes
    # [track["class_id"].max() for track in tracks]
    tracks = [track for track in tracks if track["class_id"].max() in valid_classes]
    # get number of tracks
    n = len(tracks)
    # if we have no tracks, return empty list
    if n == 0:
        return []
    if n == 1:
        return [tracks]
    # other wise we have more than one track, build the similarity matrix
    similarity_matrix = np.zeros(shape=(n, n), dtype=np.float32)
    # calculate the similarity score per pair of tracks
    for i in range(n):
        for j in range(n):
            if i > j:
                # if we detect that the tracks suffer from problem 1 described in the notion page:
                # https://www.notion.so/Tracking-Mechanisms-10652a043c5948ee98de76e8ae0c6ad4
                similarity_matrix[i][j] = calculate_similarity(tracks[i], tracks[j])

    similarity_matrix += similarity_matrix.T + np.eye(n)

    # ordering is a list of id tracks
    # ex: [0,1] means that the first track should be merged with the second track
    ordering = group_tracks(similarity_matrix, threshold=threshold)

    # tracks to merge
    if len(ordering):
        new_tracks = []
        for bag_i in ordering:
            if len(bag_i) > 1:
                new_tracks.append(merge_tracks([tracks[i] for i in bag_i]))
            else:
                new_tracks.append(tracks[bag_i[0]])
        tracks = new_tracks

    # sort tracks
    tracks = score_tracks(
        tracks, class_dependent=class_dependent, valid_classes=valid_classes
    )

    # tracks to filter out
    def is_small_track(track, threshold=0.9):
        track_dim = track["bbox"].shape[0]
        return np.any(np.isnan(track["bbox"]), axis=1).sum() / track_dim > threshold

    # filter small tracks
    tracks = [track for track in tracks if not is_small_track(track, threshold=0.95)]

    # return tracks
    return [tracks]  # if single_class else tracks


class VideoTooSmallException(Exception):
    """
    This class is used when the video is too small.
    """

    def __init__(self):
        """
        Initialize the VideoTooSmallException class.
        """

        super().__init__(message=f"Video is too small.")


class _GatherToArray(QControlledMap.QControlledFunc):
    """
    Gather an array of tracks.
    """

    def __init__(self) -> None:
        super().__init__()

    def configure(self, controls):
        controls = {key: value for key, value in controls}
        # self.size, self.shape = controls.pop("get_metadata")

        # if self.shape is None video was to small
        # if self.shape is None:
        #     raise VideoTooSmallException()

        # if len(self.shape) != 3:
        #     self.shape = (*self.shape, 3)

        self.path = controls.pop("sv_path")

        self.configs = {
            # "frame_shape": self.shape,
            # "frames": self.size,
            **controls,
        }

    def apply(self, track):
        """
        Apply gathered tracks to the base structure.
        """

        base = {
            "keypoint_coords": np.zeros((self.size, 17, 2), dtype=np.float32) * np.nan,
            "keypoint_scores": np.zeros((self.size, 17, 1), dtype=np.float32) * np.nan,
            "features": np.zeros((self.size, 512), dtype=np.float32) * np.nan,
            "volatility": np.zeros((self.size, 1), dtype=np.float32) * np.nan,
            "bbox": np.zeros((self.size, 4), dtype=np.float32) * np.nan,
            "mv_avg": np.ones((self.size, 4), dtype=np.float32),
            "class_id": np.zeros((self.size, 1), dtype=np.int),
            "tracked_time_step": np.zeros((self.size, 1), dtype=np.int),
            "score": np.zeros((self.size, 1), dtype=np.float32) * np.nan,
            "sv_path": self.path,
            "size": self.size,
            "shape": self.shape,
            "configs": self.configs,
        }

        for i, track_id, coords, scores, info in track:
            base["track_id"] = track_id

            if coords is not None:
                info["keypoint_coords"] = coords
                info["keypoint_scores"] = scores

            for k, v in info.items():
                # if v is not None:
                base[k][i] = v

        return base


class SceneUnderstandingFlow(QWorkFlow):
    """This workflow is used to merging tracks and filtering."""

    def __init__(
        self,
        merge_threshold=0.05,
    ):
        super().__init__(name="SceneUnderstandingFlow")

        self.gather = QControlledMap(
            func=_GatherToArray(),
            name="incorporate_control_info",
            # This function parameterizes a function based on a control stream and gathers to a dictionary of arrays.
        ) | QAggregate(
            key_factory=lambda x: "0",
            name="class_id_aggregate",
        )  # agregate all of the tracks for each class : big sync block.

        self.track_postprocessing = QClassicMap(
            func=lambda x: ("tracks", x), name="mark_tracks"
        )  # This  function just adds an identifier to this stream.
        # It's probably better to add this to GATHERTOARRAY.

        self.merge_threshold = merge_threshold

    def forward(
        self,
        input: QActor,
        # video_metadata: QActor,
        # endpoint_metadata: QActor,
        sport_details={
            "valid_classes": [0, 32],
            "single_class": False,
            "class_dependent": False,
        },
    ) -> QActor:
        # group_remove_similar_tracks
        pipeline = (
            self.gather
            | QFlatMap(
                func=partial(
                    group_merge_filter_and_sort_tracks,
                    threshold=self.merge_threshold,  # max similarity
                    valid_classes=sport_details["valid_classes"],
                    single_class=sport_details["single_class"],
                    class_dependent=sport_details["class_dependent"],
                )
            )  # applies merge to tracks.
            | self.track_postprocessing
        )

        tracks = pipeline(
            input
            # endpoint_metadata,
        )

        return tracks
