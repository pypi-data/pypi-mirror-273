import json
import logging
from typing import Dict, List, Optional, Tuple

from pyqflow import QStatefulBarrier, QWorkFlow
from pyqflow.actor import QActor

import json
import logging
from typing import Dict, List

# Standard Libraries
from pyqflow import QStatefulBarrier

# Import functions about Tracking
from moovs_business.utils.tracks import Detection

# Tracking functions
from moovs_business.utils.math import (
    NearestNeighborDistanceMetric,
    xyxy_to_tlwh_,
    NearestNeighborDistanceMetric,
)
from moovs_business.utils.tracks import Tracker


class TrackingState(QStatefulBarrier.QState):  # tracking module.
    # max age - number of allowed missing frames to discard a given track.
    # By default, we do not want do reject any track and resolve this pair-wise match at the end using the Hungarian algorithm
    def __init__(
        self,
        max_dist: float,
        min_confidence: float,
        max_iou_distance: float,
        max_age: int,
        n_init: Dict[str, int],
        nn_budget: Dict[str, int],
        nn_minimum_supply: Dict[str, int],
        single_class: bool,
        protected_classes: List[str],
        max_returned_tracks: Dict[str, int],
        gating_dim=Dict[str, int],
        debug: bool = False,
        **kwargs,
    ):
        # print("Deep Sort confs = ",  max_dist, min_confidence, max_iou_distance, max_age, n_init, nn_budget)
        self.time_step = 0
        self.single_class = single_class
        self.min_confidence = min_confidence
        self.max_cosine_distance = max_dist
        self.nn_budget = nn_budget
        self.n_init = n_init
        self.max_iou_distance = max_iou_distance
        self.max_age = max_age
        self.nn_minimum_supply = nn_minimum_supply
        self.protected_classes = protected_classes
        self.max_returned_tracks = max_returned_tracks
        self.gating_dim = gating_dim
        self.debug = debug  # when debug is True, the tracker will not return any candidates. It will return all the tracks
        # extract kwargs
        self.kwargs = kwargs
        self.init()

    def init(self):
        self.tracker = Tracker(
            metric=NearestNeighborDistanceMetric(
                "cosine", self.max_cosine_distance, self.nn_budget
            ),
            max_iou_distance=self.max_iou_distance,
            max_age=self.max_age,
            n_init=self.n_init,
            nn_minimum_supply=self.nn_minimum_supply,
            nn_budget=self.nn_budget,
            max_returned_tracks=self.max_returned_tracks,
            gating_dim=self.gating_dim,
        )

    # terminate the tracker
    def terminate(self):
        self.tracker.terminate()
        del self.tracker
        self.tracker = None

    # Update the tracks
    def update(self, context):
        frame_shape = None
        for frame_i_pred in context:
            detections = []
            if frame_i_pred:
                for (
                    bbox_xyxy_j,  # bbox coordinates
                    confidence_j,  # confidence of the detection
                    class_j,  # class of the detection
                    frame_shape_j,  # frame shape
                    feature_j,  # feature vector (embedding from a ReID model) of the detection
                    imcrop_descriptor_j,  # image crop of the descriptor
                    imcrop_evopose_j,  # image crop for the evpose
                    imcrop_prop_j,  # image crop properties of the detection
                ) in frame_i_pred:
                    del imcrop_descriptor_j
                    frame_shape = frame_shape_j
                    class_j = str(int(class_j))  # convert to string
                    if (
                        confidence_j > self.min_confidence
                    ):  # if the confidence is above the threshold
                        # if the class is not in the protected classes (person class),
                        # then we will not delete its croppings & properties from memory
                        # since they are not used in the Pose Estimation module
                        if class_j not in self.protected_classes:
                            del imcrop_evopose_j
                            del imcrop_prop_j
                            imcrop_prop_j, imcrop_evopose_j = None, None

                        # append the detection to the list of detections
                        detections.append(
                            Detection(
                                tlwh=xyxy_to_tlwh_(bbox_xyxy_j),
                                confidence=confidence_j,
                                feature=feature_j,
                                # crops_descriptor=imcrop_descriptor_j,
                                crops_evopose=imcrop_evopose_j,
                                crop_properties=imcrop_prop_j,
                                class_id=class_j,
                            )
                        )
                # if no detection is considered valid - score > self.min_confidence increment age of all tracks
                if len(detections) == 0:
                    self.tracker.increment_ages()
                else:
                    # increment tracker prediction
                    # a new mean and covariance are computed to use with the kalman filter
                    self.tracker.predict()
                    # update the tracker with the new detections
                    self.tracker.update(
                        detections=detections,
                        time_step=self.time_step,
                    )
            else:
                # increment ages when no objects are detected (basically, increment the age of all tracks)
                self.tracker.increment_ages()

            self.time_step += 1

        if frame_shape is None:
            return []

        p_outputs = self.tracker.return_pose_candidates(frame_shape)
        b_outputs = self.tracker.return_ball_candidates(frame_shape)

        return p_outputs + b_outputs


class TrackFlow(QWorkFlow):
    """This workflow is used to track objects in a video."""

    def __init__(
        self,
        max_dist: float = 0.2,  # maximum distance of cosine similrity between the features descriptors of different objects
        min_confidence: float = 0.2,  # min confidence for the detection of an object
        max_iou_distance: float = 0.7,  # max iou distance between bounding boxes
        max_age: int = 30
        * 30,  # if the track does not appear for 30 seconds, it is deleted
        n_init: Dict[str, int] = {
            "0": 7,
            "32": 4,
        },  # number of consecutive detections before initializing a track
        nn_budget: Dict[str, int] = {"0": 50, "32": 50},
        nn_minimum_supply: Dict[str, int] = {
            "0": 30 * 5,
            "32": 17,
        },  # minimum supply for this track to be accepted as candidate
        single_class: bool = True,  # track all objets per class, or only the most confident one per class
        protected_classes: List[str] = ["0"],  # get's passed to pose.
        max_returned_tracks: Dict[str, int] = {
            "0": 1,
            "32": 500,
        },  # return a max of X tracks for each class
        gating_dim: Dict[str, int] = {
            "0": 6,
            "32": 4,
        },  # gating dimension represents the degree of freedom passed into the Chi-squared distribution according to each class space of motion
        debug: bool = False,
    ):
        """
        Initialize the TrackFlow workflow.

        Args:
            max_dist (float, optional): Maximum distance of cosine similarity between the features descriptors of different objects. Defaults to 0.15.
            min_confidence (float, optional): Minimum confidence for the detection of an object. Defaults to 0.2.
            max_iou_distance (float, optional): Maximum IOU distance between bounding boxes. Defaults to 0.7.
            max_age (int, optional): If the track does not appear for 5 seconds, it is deleted. Defaults to 30 * 5.
            n_init (Dict[str, int], optional): Number of consecutive detections before initializing a track. Defaults to {"0": 10, "32": 4}.
            nn_budget (Dict[str, int], optional): Budget for the nearest neighbors. Defaults to {"0": 100, "32": 200}.
            nn_minimum_supply (Dict[str, int], optional): Minimum supply of nearest neighbors. Defaults to {"0": 30 * 5, "32": 0}.
            single_class (bool, optional): Track all objects per class, or only the most confident one per class. Defaults to True.
            protected_classes (List[str], optional): Protected classes to be passed to the pose. Defaults to ["0"].
            max_returned_tracks (Dict[str, int], optional): Return a maximum of X tracks for each class. Defaults to {"0": 1, "32": 100}.
            gating_dim (Dict[str, int], optional): Gating dimension represents the degree of freedom passed into the Chi-squared distribution according to each class's space of motion. Defaults to {"0": 2, "32": 4}.
            debug (bool, optional): Enable debugging mode. Defaults to False.
        """
        super().__init__(name="Track")
        self.params = {
            "max_dist": max_dist,
            "min_confidence": min_confidence,
            "max_iou_distance": max_iou_distance,
            "max_age": max_age,
            "n_init": n_init,
            "nn_budget": nn_budget,
            "nn_minimum_supply": nn_minimum_supply,
            "single_class": single_class,
            "protected_classes": protected_classes,
            "max_returned_tracks": max_returned_tracks,
            "gating_dim": gating_dim,
            "debug": debug,
        }

    def forward(self, input: QActor) -> QActor:
        """Process input using the TrackingState.

        Args:
            input (Any): Input data to be processed.

        Returns:
            Any: Processed output data.
        """

        # if self.progression_track is defined pass it to the TrackingState
        self.barrier = QStatefulBarrier(
            functional=TrackingState(**self.params),
            name="Barrier:Tracking",
        )

        barrier_out = self.barrier(input)
        return barrier_out
