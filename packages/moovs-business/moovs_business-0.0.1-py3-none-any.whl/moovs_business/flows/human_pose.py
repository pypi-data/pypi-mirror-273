from typing import List

from pyqflow import (
    QAggregate,
    QBatching,
    QClassicMap,
    QRemoteMap,
    QUnBatching,
    QWorkFlow,
    QNativeMap,
    QCallback,
    QVideo,
)
from pyqflow.actor import QActor
from functools import partial
from moovs_business.utils.helpers import scale_pose_predictions, extract_crops
from moovs_business.utils.serialize import arranging_pose_inputs
from moovs_business.constants import URL, MOOVS_BUSINESS_API_KEY
from moovs_business.flows.tracking import TrackingFlow
from moovs_business.utils.pose import SceneUnderstandingFlow
import numpy as np
import random
from moovs_business.structs import BoundingBoxes, BoundingBox, BoundingBoxesSequences


class _AtomPoseFlow(QWorkFlow):
    """This workflow is used to perform pose estimation."""

    def __init__(
        self,
        ch: bool = False,
        batch_size: int = 8,
        endpoint: str = "pose_estimation",
        host: str = URL,
        img_size: List[int] = [384, 288],
        **kwargs,
    ):
        """
        Initialize the PoseFlow class.

        Args:
            ch (bool, optional): Channel first. Defaults to False.
            batch_size (int, optional): Batch size. Defaults to 8.
            endpoint (str, optional): Endpoint. Defaults to "pose_estimation".
            host (str, optional): Host. Defaults to "http://127.0.0.1:8000".
            img_size (List[int], optional): Image size. Defaults to [384, 288].
        """
        super().__init__(name="Pose")

        self.batch = batch_size
        self.endpoint = f"{host}/{endpoint}"
        self.ch = ch
        self.input_size = img_size

        # Resize to fit pose estimation model
        self.object_resize = QNativeMap(
            name="extract-crops:384x288",
            many=True,
            func=partial(
                extract_crops,
                output_shape=img_size,
                context_scale=2.0,
            ),
        )

        # Mechanism to handle human pose estimation
        self._detection_pipeline = (
            QBatching(
                self.batch,
                select=(lambda data: data[-2] is not None),
                name="Pose:Batching",
            )  # Creates batches of images.
            | QClassicMap(
                name="arranging_pose_inputs",
                func=arranging_pose_inputs,
            )  # Preprocess the images
            | QRemoteMap(
                url=self.endpoint,
                pack_function=lambda data: [data[0].tobytes(), data[1]],
                unpack_function=scale_pose_predictions,
                name="Pose:Request",
                many=False,
                headers={
                    "x-api-key": MOOVS_BUSINESS_API_KEY,
                },
            )  # Send the data to the remote server
        )

        self._unload_pipeline = QUnBatching(
            name="Pose:UnBatching"
        ) | QAggregate(  # Unbatch the predictions
            key_factory=lambda data: str(data[1]), name="track_aggregate"
        )  # Aggregate the predictions by track : This is a big sync block.

    def forward(self, input: QActor) -> QActor:
        """
        Process the input through the pose estimation pipeline.

        Args:
            input: The input data.

        Returns:
            np.ndarray: Pose estimation output.
        """
        # [ ((idx track, idx frame, im crop, crop properties), id ), ...]
        extended_pipeline = self._detection_pipeline | self._unload_pipeline

        output = extended_pipeline(input)

        return output


class PoseFlow(QWorkFlow):
    """This workflow is used to perform pose estimation."""

    def __init__(self):
        # Track each of the individuals
        self.tracking = TrackingFlow()

        # To process human pose estimation
        self.pose = _AtomPoseFlow()

    def forward(self, source: QVideo) -> QActor:
        if not isinstance(source, QVideo):
            raise ValueError("The source must be a QVideo object.")

        tracks = self.tracking.forward(source)

        # predict the poses using said tracks
        pose_preds = self.pose.forward(tracks)

        return pose_preds

    async def __call__(self, source: QVideo) -> BoundingBoxesSequences:
        res = await super().__call__(source)

        # Created a random color for each available track
        rand_colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for i in range(len(res[0]))
        ]

        def validate_v(v):
            return not np.any(np.isnan(v[-1]["bbox"])) and v[3] is not None

        # Unwrap all of the bounding boxes
        data = [
            {
                "frame": v[0],
                "track_id": v[1],
                "kps": v[2],
                "kp_scores": v[3],
                "class_id": v[-1]["class_id"],
                "bbox": v[-1]["bbox"],
                "score": v[-1]["score"],
                "rand_color": rand_colors[idx],
            }
            for idx, x in enumerate(res[0])
            for v in x[1]
            if validate_v(v)
        ]

        # Group by frame numbers
        data_by_frame = {}

        for v in data:
            if v["frame"] not in data_by_frame:
                data_by_frame[v["frame"]] = []

            data_by_frame[v["frame"]].append(v)

        # Now organize it as a list of bounding boxes
        bounding_boxes = {
            k: BoundingBoxes(
                bboxes=[
                    BoundingBox(
                        top=v["bbox"][0],
                        left=v["bbox"][1],
                        bottom=v["bbox"][2],
                        right=v["bbox"][3],
                        color=v["rand_color"],
                        extra_data={
                            "track_id": v["track_id"],
                            "class_id": v["class_id"],
                            "score": v["score"],
                            "kps": v["kps"],
                            "kp_scores": v["kp_scores"],
                        },
                    )
                    for v in data_by_frame[k]
                ]
            )
            for k in data_by_frame.keys()
        }

        # Select the max id
        max_id = max(bounding_boxes.keys())

        # Now create the bounding boxes listing with filler spaces if needed
        bboxes = BoundingBoxesSequences(
            bboxes=[
                bounding_boxes[k] if k in bounding_boxes else BoundingBoxes(bboxes=[])
                for k in range(max_id + 1)
            ]
        )

        return bboxes
