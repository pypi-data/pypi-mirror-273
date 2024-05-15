from pyqflow import QWorkFlow, QNativeMap, QBatching, QClassicMap
from moovs_business.utils.serialize import arranging_pose_inputs
from pyqflow.actor import QImage, QVideo, QActor
from moovs_business.flows.detection import DetectionFlow
from functools import partial
from moovs_business.utils.helpers import extract_crops
from moovs_business.flows.subs.descriptor import DescriptorFlow
from moovs_business.flows.subs.tracks import TrackFlow
from typing import Union, Tuple, Any
import numpy as np
import random
from moovs_business.structs import BoundingBoxes, BoundingBox, BoundingBoxesSequences


class TrackingFlow(QWorkFlow):
    def __init__(self):
        super().__init__(name="Tracking")

        # Need to use the detection flow to get the bounding boxes
        self.detection = DetectionFlow()

        # Use object resizer for each of the individuals
        self.object_resize = QNativeMap(
            name="extract-crops:384x288",
            many=True,
            func=partial(
                extract_crops,
                output_shape=[384, 288],
                context_scale=2.0,
            ),
        )

        # Descriptor flow - used to get the context vectors
        self.descriptor = DescriptorFlow(
            batch_size=16,
        )

        # Track flow - used to arrange predictions into cohesive tracks
        self.tracker = TrackFlow()

    def forward(self, source: QVideo) -> QActor:
        if not isinstance(source, QVideo):
            raise ValueError("The source must be a QVideo object.")

        # obtain object predictions from the detection model
        bbox_prediction = self.detection.forward(source)

        # crops the bounding boxes from the original image
        object_crops = self.object_resize(bbox_prediction)

        # obtain object descriptors from the descriptor model
        context_vectors = self.descriptor.forward(object_crops)

        # arranges the predictions into cohesive tracks.
        tracks = self.tracker.forward(context_vectors)

        return tracks

    async def __call__(self, source: QVideo) -> BoundingBoxesSequences:
        res = await super().__call__(source)

        data = [
            {
                "frame": v[1][0],
                "track_id": v[1][1],
                "class_id": v[1][-1]["class_id"],
                "bbox": v[1][-1]["bbox"],
                "score": v[1][-1]["score"],
            }
            for v in res[0]
            if not np.any(np.isnan(v[1][-1]["bbox"]))
        ]

        # Group by frame numbers
        data_by_frame = {}

        for v in data:
            if v["frame"] not in data_by_frame:
                data_by_frame[v["frame"]] = []

            data_by_frame[v["frame"]].append(v)

        # Keep track of all of the track ids
        track_ids = set(v["track_id"] for v in data)
        rand_colors = {
            k: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for k in track_ids
        }

        # Now organize it as a list of bounding boxes
        bounding_boxes = {
            k: BoundingBoxes(
                bboxes=[
                    BoundingBox(
                        top=v["bbox"][0],
                        left=v["bbox"][1],
                        bottom=v["bbox"][2],
                        right=v["bbox"][3],
                        color=rand_colors[v["track_id"]],
                        extra_data={
                            "track_id": v["track_id"],
                            "class_id": v["class_id"],
                            "score": v["score"],
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
