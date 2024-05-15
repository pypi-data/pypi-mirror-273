import numpy as np
from typing import Dict, Tuple
from moovs_business.tracking import kalman_filter, linear_assignment, iou_matching
import itertools
from moovs_business.tracking.moving_average import VolatilityTracker
from moovs_business.utils.math import score_ball, score_person


class Detection:
    """
    This class represents a bounding box detection in a single image.

    Parameters
    ----------
    tlwh : array_like
        Bounding box in format `(x, y, w, h)`.
    confidence : float
        Detector confidence score.
    feature : array_like
        A feature vector that describes the object contained in this image.

    Attributes
    ----------
    tlwh : ndarray
        Bounding box in format `(top left x, top left y, width, height)`.
    confidence : ndarray
        Detector confidence score.
    feature : ndarray | NoneType
        A feature vector that describes the object contained in this image.

    """

    def __init__(
        self, tlwh, confidence, feature, crops_evopose, crop_properties, class_id
    ):
        self.tlwh = tlwh
        self.confidence = float(confidence)
        self.feature = feature
        self.im_crop_evo = crops_evopose
        # self.im_crop_desc = crops_descriptor
        self.crop_properties = crop_properties
        self.class_id = class_id

    def to_tlbr(self):
        """Convert bounding box to format `(min x, min y, max x, max y)`, i.e.,
        `(top left, bottom right)`.
        """
        ret = self.tlwh.copy()
        ret[2:] += ret[:2]
        return ret

    def to_blwh(self):
        """Get current position in bounding box format `(bot left x, bot left y,
        width, height)`.

        Returns
        -------
        ndarray
            The bounding box.

        """
        ret = self.tlwh.copy()
        ret[1] -= ret[3]
        return ret

    def to_xyah(self):
        """Convert bounding box to format `(center x, center y, aspect ratio,
        height)`, where the aspect ratio is `width / height`.
        """
        ret = self.tlwh.copy()
        ret[:2] += ret[2:] / 2
        ret[2] /= ret[3]
        return ret

    def isnan(self):
        return np.isnan(self.tlwh).any()


class TrackState:
    """
    Enumeration type for the single target track state. Newly created tracks are
    classified as `tentative` until enough evidence has been collected. Then,
    the track state is changed to `confirmed`. Tracks that are no longer alive
    are classified as `deleted` to mark them for removal from the set of active
    tracks.

    """

    Tentative = 1
    Confirmed = 2
    Deleted = 3


class Track:
    """
    A single target track with state space `(x, y, a, h)` and associated
    velocities, where `(x, y)` is the center of the bounding box, `a` is the
    aspect ratio and `h` is the height.

    Parameters
    ----------
    mean : ndarray
        Mean vector of the initial state distribution.
    covariance : ndarray
        Covariance matrix of the initial state distribution.
    track_id : int
        A unique track identifier.
    n_init : int
        Number of consecutive detections before the track is confirmed. The
        track state is set to `Deleted` if a miss occurs within the first
        `n_init` frames.
    max_age : int
        The maximum number of consecutive misses before the track state is
        set to `Deleted`.
    feature : Optional[ndarray]
        Feature vector of the detection this track originates from. If not None,
        this feature is added to the `features` cache.

    Attributes
    ----------
    mean : ndarray
        Mean vector of the initial state distribution.
    covariance : ndarray
        Covariance matrix of the initial state distribution.
    track_id : int
        A unique track identifier.
    hits : int
        Total number of measurement updates.
    age : int
        Total number of frames since first occurance.
    time_since_update : int
        Total number of frames since last measurement update.
    state : TrackState
        The current track state.
    features : List[ndarray]
        A cache of features. On each measurement update, the associated feature
        vector is added to this list.

    """

    def __init__(
        self,
        particle_filter: kalman_filter.KalmanFilter,
        track_id: int,
        class_id: str,
        time_step: int,
        n_init: int,
        max_age: int,
        nn_budget: int,
    ):
        self.particle_filter = particle_filter
        self.mean, self.covariance = 0, 0
        self.index_crop, self.count = 0, 0
        self.track_id = track_id
        self.class_id = class_id
        self.hits, self.age, self.time_since_update = 1, 1, 0
        self.state = TrackState.Tentative
        self.features, self.volatility = (
            [],
            [],
        )  # tracking of the object features
        self.detections = []
        self.pose_ = []  # tracking keypoints and keypoint scores for every person class
        self.tracked_time_step = time_step
        # keep a tracking of the last tracked positions, associated scores

        self.ma_volatility = VolatilityTracker(
            growth_factor=2.2, beta=0.4, bias_correction=True, start_std=100, eps=1e-4
        )

        for _ in range(self.tracked_time_step):
            self.volatility.append(0)
            self.detections.append(None)
            self.pose_.append((None, None))
            self.count += 1
            self.ma_volatility.target_delay()

        self._n_init = n_init
        self._max_age = max_age
        self.nn_budget = nn_budget

    def start(
        self,
        detection: Detection,
    ):
        return self.update(detection, first=True)

    def terminate(self):
        for d in self.detections:
            del d

        for f in self.features:
            del f

        del self.detections

    def update(
        self,
        detection: Detection,
        first: bool = False,
    ):
        self.count += 1
        self.detections.append(detection)  # bbox.to_tlbr(),
        self.features.append(detection.feature)

        if first:
            self.mean, self.covariance = self.particle_filter.initiate(
                detection.to_xyah()
            )
            self.volatility.append(0)
            self.hits = 1
            self.time_since_update = 0
            self.state = TrackState.Tentative

        else:
            self.mean, self.covariance, volatility = self.particle_filter.update(
                self.mean, self.covariance, detection.to_xyah()
            )
            self.volatility.append(volatility)
            self.hits += 1
            self.time_since_update = 0

            if detection.isnan():
                self.ma_volatility.target_missing()  # update volatility measure as missing
            else:
                self.ma_volatility.target_update(
                    detection.to_tlbr().reshape(2, 2), volatility
                )

        # change the track state according to business properties
        # 1. A Track is accepted if:
        #  - The previous state = Tentative
        #  - The number of hits/times this track/object appeared is > _n_init
        # 2. A Track is considered Candidate if:
        #  - Is confirmed
        #  - The track is representative of a person
        if self.state == TrackState.Tentative and self.hits >= self._n_init:
            # here the track is accepted and confirmed as an Identity
            self.state = TrackState.Confirmed

        return self

    def to_tlwh(self):
        """Get current position in bounding box format `(top left x, top left y,
        width, height)`.

        Returns
        -------
        ndarray
            The bounding box.

        """
        ret = self.mean[:4].copy()
        ret[2] *= ret[3]
        ret[:2] -= ret[2:] / 2
        return ret

    def to_blwh(self):
        """Get current position in bounding box format `(bot left x, bot left y,
        width, height)`.

        Returns
        -------
        ndarray
            The bounding box.

        """
        ret = self.to_tlwh()
        ret[1] -= ret[3]
        return ret

    def to_tlbr(self):
        """Get kf estimated current position in bounding box format `(min x, miny, max x,
        max y)`.

        Returns
        -------
        ndarray
            The predicted kf bounding box.

        """
        ret = self.to_tlwh()
        ret[2:] = ret[:2] + ret[2:]
        return ret

    def increment_age(self):
        self.age += 1
        self.time_since_update += 1

    def predict(self):
        """Propagate the state distribution to the current time step using a
        Kalman filter prediction step.

        Parameters
        ----------
        kf : kalman_filter.KalmanFilter
            The Kalman filter.

        """
        self.mean, self.covariance = self.particle_filter.predict(
            self.mean, self.covariance
        )
        self.increment_age()

    def mark_missed(self):
        """Mark this track as missed (no association at the current time step)."""
        if self.state == TrackState.Tentative:
            self.state = TrackState.Deleted
        elif self.time_since_update > self._max_age:
            self.state = TrackState.Deleted
        # Update track
        nan_ = float("nan")

        self.detections.append(None)
        self.ma_volatility.target_delay()
        self.volatility.append(nan_)
        self.count += 1

    def is_tentative(self):
        """Returns True if this track is tentative (unconfirmed)."""
        return self.state == TrackState.Tentative

    def is_confirmed(self):
        """Returns True if this track is confirmed."""
        return self.state == TrackState.Confirmed

    def is_candidate(self, nn_minimum_supply, class_id="0"):
        # minimum supply for this track to be accepted as candidate
        """Returns True if this track is a candidate to PoseEstimation inference"""

        return (
            self.state == TrackState.Confirmed
            and self.class_id == class_id  # Person
            and self.hits
            >= nn_minimum_supply  # minimum supply for this track to be accepted as candidate
        )

    def is_deleted(self):
        """Returns True if this track is dead and should be deleted."""
        return self.state == TrackState.Deleted

    def __get__(self, key):
        try:
            return self.__getattribute__(key)
        except Exception as _:
            return None

    def __info__(self):
        return {
            "track_id": self.track_id,
            "hits": self.hits,
            "time_since_update": self.time_since_update,
            "state": self.state,
            "tracked_time_step": self.tracked_time_step,
            "n_init": self._n_init,
            "max_age": self._max_age,
        }

    def value(self, frame_shape: Tuple):
        """
        Calculates the value of the track.
        The closest this value is to 1, the higher the chances of  this track representing a "VIP track".
        In total there are two types of tracks:
            - Tracks that represents object of interest (VIP Tracks)
                - In Football this can be tought as, the person doing freestyle with a ball (in this case, this ball is also considered another VIP track)
            - Tracks that represent additional objects:
                - Background objects
                - MissClassified Objects (by the object detection method)
                - New objects originated by exclusion of the kalman filter
                    - Examples of this are objects with sudden movements.
                    This objects are filtered out by the Kalman Filter part, since the difference of the expected position and the actual one is to far.
        VIP track, is considered tracks of objects of interest.
        """
        # This value is calculated by:
        # 1. The mean score
        # 2. The percentage difference between the cropping area of the object, and the total image area
        # 3. The missing rate

        tracked_positions = [d.to_tlbr() for d in self.detections if d]  #
        tracked_scores = [d.confidence for d in self.detections if d]  #

        if self.class_id == "32":
            return score_ball(tracked_positions, tracked_scores)
        elif self.class_id == "0":
            return score_person(tracked_positions, tracked_scores, frame_shape)
        else:
            raise Exception(f"Unknown class id {self.class_id}.")

    def add_keypoints_inference(self, results):
        self.pose_.extend(results)

    def extract_info(self):
        # Return the following [(frame_id, track_id, im_crop), (...), ...]
        res = []
        diff = self.count - self.index_crop

        # box
        for _ in range(diff):
            detection = self.detections.pop(0)
            mv_volatility, mv_avg, mv_std = self.ma_volatility.pop(0)

            if detection:
                features = detection.feature
                score = detection.confidence
                im_crop_evopse = detection.im_crop_evo
                # im_crop_descriptor = detection.im_crop_desc
                crops_properties = detection.crop_properties
                bbox = detection.to_tlbr()

            else:
                features = None
                im_crop_evopse = None
                im_crop_descriptor = None
                crops_properties = None
                bbox = np.array([np.nan] * 4)
                score = 0.0

            res.append(
                (
                    self.index_crop,
                    self.track_id,
                    # im_crop_descriptor,
                    im_crop_evopse,
                    crops_properties,
                    {
                        "features": features,
                        "volatility": mv_volatility,
                        "score": score,
                        "bbox": bbox,
                        "class_id": int(self.class_id),
                        "tracked_time_step": self.tracked_time_step,
                        "mv_avg": mv_avg.reshape(-1, 4),
                    },
                )  # actual volatility & moving average missing.
            )

            self.index_crop += 1

        # add index
        return res


class Tracker:
    """
    This is the multi-target tracker.

    Parameters
    ----------
    metric : nn_matching.NearestNeighborDistanceMetric
        A distance metric for measurement-to-track association.
    max_age : int
        Maximum number of missed misses before a track is deleted.
    n_init : int
        Number of consecutive detections before the track is confirmed. The
        track state is set to `Deleted` if a miss occurs within the first
        `n_init` frames.

    Attributes
    ----------
    metric : nn_matching.NearestNeighborDistanceMetric
        The distance metric used for measurement to track association.
    max_age : int
        Maximum number of missed misses before a track is deleted.
    n_init : int
        Number of frames that a track remains in initialization phase.
    kf : kalman_filter.KalmanFilter
        A Kalman filter to filter target trajectories in image space.
    tracks : List[Track]
        The list of active tracks at the current time step.

    """

    def __init__(
        self,
        metric,
        max_iou_distance: float = 0.8,
        max_age: Dict[str, int] = {"0": 30 * 5, "32": 0},
        n_init: Dict[str, int] = {"0": 3, "32": 3},
        nn_minimum_supply: int = 100,
        nn_budget: Dict[str, int] = {"0": 50, "32": 50},
        max_returned_tracks: Dict[str, int] = {"0": 1, "32": 100},
        gating_dim={"0": 2, "32": 4},
    ):
        self.metric = metric
        self.max_iou_distance = max_iou_distance
        self.max_age = max_age
        self.n_init = n_init
        self.kf = kalman_filter.KalmanFilter()
        self.tracks = []
        self.nn_minimum_supply = nn_minimum_supply
        self._next_id = 1
        self.nn_budget = nn_budget
        self.max_returned_tracks = max_returned_tracks
        self.gating_dim = gating_dim

    def predict(self):
        """Propagate track state distributions one time step forward.

        This function should be called once every time step, before `update`.
        """
        for track in self.tracks:
            track.predict()

    def increment_ages(self):
        for track in self.tracks:
            track.increment_age()
            track.mark_missed()

    def terminate(self):
        for track in self.tracks:
            track.terminate()

        self.metric.terminate()

    def update(self, detections, time_step):
        """[Perform measurement update and track management.]

        Args:
            detections ([type]): List[deep_sort.detection.Detection]
            A list of detections at the current time step.
            scores ([type]): A list of scores of each detection.
            classes ([type]): A list of classes of each detection.
            time_step ([type]): A list of time steps of each detection.
        """

        # Run matching cascade.
        matches, unmatched_tracks, unmatched_detections = self._match(
            detections, debug=False
        )

        """
        logging.info(
            "We have {} tracks.\n\
            From {} detections\
            We have {} matches,\
            {} unmatched tracks\
            and {} unmatched detections".format(
                len(self.tracks),
                len(detections),
                len(matches),
                len(unmatched_tracks),
                len(unmatched_detections),
            )
        )
        """

        # Update track set.
        # tracked matches with confirmed tracks (associated trackes with tracked positions > n_init)
        for track_idx, detection_idx in matches:
            detection = detections[detection_idx]
            self.tracks[track_idx].update(detection)
        # unmatched_tracks. tracked identities where no associated objects were detected (in the current step)
        for track_idx in unmatched_tracks:
            self.tracks[track_idx].mark_missed()

        # unmatch detection (new objects) result in new identities
        for detection_idx in unmatched_detections:
            detection = detections[detection_idx]

            self._initiate_track(
                detection,
                time_step,
            )

        # deleted tracks are removed from equation
        self.tracks = [t for t in self.tracks if not t.is_deleted()]

        # Update distance metric
        active_targets = [t.track_id for t in self.tracks if t.is_confirmed()]

        features, targets = [], []
        target_classes = []

        for _, track in enumerate(self.tracks):
            if not track.is_confirmed():
                continue
            features += track.features
            targets += [track.track_id for _ in track.features]
            target_classes += [track.class_id for _ in track.features]
            track.features = []

        # Add the new features
        self.metric.partial_fit(
            np.asarray(features), np.asarray(targets), active_targets, target_classes
        )

    def return_pose_tracks(self, *args, **kwargs):
        return self.return_tracks(class_id="0")

    def return_ball_tracks(self, *args, **kwargs):
        return self.return_tracks(class_id="32")

    def return_tracks(self, class_id="0"):
        """[summary]

        Args:
            class_id (str, optional): [description]. Defaults to "0".

        Returns:
            [type]: [description]
        """
        # return tracks with class_id
        tracks = [t for t in self.tracks if t.class_id == class_id]
        outputs = list(itertools.chain(*[track.extract_info() for track in tracks]))
        return outputs

    def return_candidate_tracks(self, class_id="0"):
        candidate_tracks = [
            track
            for track in self.tracks
            if track.is_candidate(
                nn_minimum_supply=self.nn_minimum_supply[class_id], class_id=class_id
            )
        ]

        return candidate_tracks

    def return_deleted_tracks(self, class_id="0"):
        candidate_tracks = [
            track
            for track in self.tracks
            if not track.is_candidate(
                nn_minimum_supply=self.nn_minimum_supply[class_id], class_id=class_id
            )
        ]
        return candidate_tracks

    def return_candidates(self, original_frame_shape, class_id="0"):
        candidate_tracks = self.return_candidate_tracks(class_id=class_id)

        candidate_tracks_scores = [
            track.value(original_frame_shape) for track in candidate_tracks
        ]

        outputs = []
        if len(candidate_tracks_scores) > 0:
            idx = list(reversed(np.argsort(candidate_tracks_scores)))[
                0 : self.max_returned_tracks[class_id]
            ]
            candidate_tracks = [candidate_tracks[idx_] for idx_ in idx]
            outputs = list(
                itertools.chain(*[track.extract_info() for track in candidate_tracks])
            )

        return outputs

    def return_pose_candidates(self, *args, **kwargs):
        # np.isnan(sv["people/38/bbox/values"]).any(axis=1)
        return self.return_candidates(*args, **kwargs, class_id="0")

    def return_ball_candidates(self, *args, **kwargs):
        return self.return_candidates(*args, **kwargs, class_id="32")

    def _match(self, detections, debug=False):
        def gated_metric(tracks, dets, track_indices, detection_indices, debug=False):
            # features = np.array([dets.feature for dets in detections])
            # targets = np.array([track.track_id for track in self.tracks])
            features = np.array([dets[i].feature for i in detection_indices])
            targets = np.array([tracks[i].track_id for i in track_indices])
            # appearance desriptor similarity
            cost_matrix = self.metric.distance(features, targets, debug=debug)

            # distance similarity
            cost_matrix = linear_assignment.gate_cost_matrix(
                self.kf,
                cost_matrix,
                tracks,
                dets,
                track_indices,
                detection_indices,
                gating_dim=self.gating_dim,
                debug=debug,
            )

            return cost_matrix

        # Split track set into confirmed and unconfirmed tracks.
        # confirmed tracks
        confirmed_tracks = [i for i, t in enumerate(self.tracks) if t.is_confirmed()]
        # unconfirmed tracks
        unconfirmed_tracks = [
            i for i, t in enumerate(self.tracks) if not t.is_confirmed()
        ]

        # Associate confirmed tracks using appearance features & kalman.
        (
            matches_a,
            unmatched_tracks_a,
            unmatched_detections,
        ) = linear_assignment.matching_cascade(
            gated_metric,
            self.metric.matching_threshold,
            self.max_age,
            self.tracks,
            detections,
            confirmed_tracks,
            debug=debug,
        )

        # Associate remaining tracks together with unconfirmed tracks using IOU.
        iou_track_candidates = unconfirmed_tracks + [
            k for k in unmatched_tracks_a if self.tracks[k].time_since_update == 1
        ]
        unmatched_tracks_a = [
            k for k in unmatched_tracks_a if self.tracks[k].time_since_update != 1
        ]

        (
            matches_b,
            unmatched_tracks_b,
            unmatched_detections,
        ) = linear_assignment.min_cost_matching(
            iou_matching.iou_cost,
            self.max_iou_distance,
            self.tracks,
            detections,
            iou_track_candidates,
            unmatched_detections,
        )

        matches = matches_a + matches_b
        unmatched_tracks = list(set(unmatched_tracks_a + unmatched_tracks_b))
        return matches, unmatched_tracks, unmatched_detections

    def add_keypoints_inference(self, track_id, results):
        for track in self.tracks:
            if track.track_id == track_id:
                track.add_keypoints_inference(results)

    def restart_tracker(self):
        self.tracks = []
        self._next_id = 1

    def _initiate_track(self, detection: Detection, time_step: int):
        class_id = detection.class_id
        # print(f"Initializing one track for class {class_id} at {time_step} step wih id = {self._next_id}")
        self.tracks.append(
            Track(
                particle_filter=self.kf,
                track_id=self._next_id,
                class_id=class_id,  # keep a tracking update
                time_step=time_step,  # track time step initialization
                n_init=self.n_init[class_id],
                max_age=self.max_age,
                nn_budget=self.nn_budget[class_id],
            ).start(detection)
        )
        self._next_id += 1
