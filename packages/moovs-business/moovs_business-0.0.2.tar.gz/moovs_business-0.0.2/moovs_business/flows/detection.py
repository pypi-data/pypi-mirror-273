# Standard Libraries
from typing import Union
from typing import List, Tuple, Any
import numpy as np
from moovs_business.constants import URL
from pyqflow import QRemoteMap, QWorkFlow, QClassicMap
from pyqflow.actor import QActor, QImage, QVideo

from moovs_business.utils.helpers import scale_bounding_box_predictions
from functools import partial
from moovs_business.utils.resize import resize_and_serialize

from moovs_business.structs import BoundingBox, BoundingBoxes, BoundingBoxesSequences
from moovs_business.constants import MOOVS_BUSINESS_API_KEY


def pack_to_object_detection(x):
    return (
        np.transpose(x[0], [0, 3, 1, 2]).tobytes(),
        x[1],
        x[2],
    )


class DetectionFlow(QWorkFlow):
    """
    This workflow implements the object detection pipeline. It takes in batches and returns a list of bounding boxes for each frame.
    """

    def __init__(
        self,
        fps: int = 30,
        ch: bool = False,
        img_size: List[int] = [640, 640],
        batch_size: int = 4,
        endpoint: str = "object_detection",
        host: str = URL,
        **kwargs,
    ):
        """
        Initialize the DetectionFlow class.

        Args:
            fps (int, optional): Frames per second. Defaults to 30.
            ch (bool, optional): Channel first. Defaults to False.
            img_size (List[int], optional): Image size. Defaults to [640, 640].
            batch_size (int, optional): Batch size. Defaults to 8.
            endpoint (str, optional): Endpoint. Defaults to "object_detection".
            host (str, optional): Host. Defaults to "http://127.0.0.1:8000"
        """

        super().__init__(name="Detection")
        self.fps = fps
        self.input_size = img_size
        self.batch = batch_size
        self.endpoint = f"{host}/{endpoint}"
        self.ch = ch

        # Required to resize the input to the correct size
        self.resize = QClassicMap(
            func=partial(
                resize_and_serialize,
                input_size=self.input_size,
                resize_info=True,
            ),
            name="resize:to:640x640",
        )

        # Pipeline to send out request to the endpoint
        self.detection = QRemoteMap(  # This sends the data to the remote server
            url=self.endpoint,
            pack_function=pack_to_object_detection,  # pack the image into a byte array
            unpack_function=lambda data, outputs, args: (
                data[3],
                scale_bounding_box_predictions(
                    outputs, *args, frame_shape=data[3].shape[1:-1]
                ),
            ),  # unpack the results
            name="Detector:Request",
            many=False,
            headers={
                "x-api-key": MOOVS_BUSINESS_API_KEY,
            },
        )

    def forward(self, source: Union[QImage, QVideo]) -> QActor:
        """
        Process the input through the detection pipeline.

        Args:
            input: The input data, can be a single frame or a batch of frames, a path to an image or a video, or a URL.

        Returns:
            The detection context.
        """
        if isinstance(source, QVideo):
            source.batch = 4  # Needs to be the same as the detection flow input

        resized_image = self.resize(source)
        return self.detection(resized_image)

    async def __call__(
        self, source: Union[QImage, QVideo]
    ) -> Union[BoundingBoxesSequences, BoundingBoxes]:
        res = await super().__call__(source)

        def sort_by_video_index(x: Tuple[str, Any]):
            # If x is all digits, then convert to int
            if x[0].isdigit():
                return int(x[0])

            return 0  # sort disabled

        bboxes = [
            (
                BoundingBoxes(
                    bboxes=[
                        BoundingBox(
                            top=v[0],
                            left=v[1],
                            bottom=v[2],
                            right=v[3],
                        )
                        for v in x
                    ]
                )
                if x is not None
                else BoundingBoxes(bboxes=[])
            )
            for point, (_, y) in sorted(res[-1], key=sort_by_video_index)
            for x in y
        ]

        if isinstance(source, QImage):
            return bboxes[0]

        return BoundingBoxesSequences(
            bboxes=bboxes,
        )
