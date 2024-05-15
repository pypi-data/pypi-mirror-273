# Standard Libraries
from typing import Sequence, Optional, Tuple
import numpy as np
from pyqflow.actor import QImage, QVideo

from pydantic import BaseModel
import cv2
import asyncio
from concurrent.futures import ThreadPoolExecutor


def any_nans(iterable_content) -> bool:
    return any(np.isnan(xx).any() for xx in iterable_content)


def to_int_tuple(iterable_content) -> Tuple[int, int]:
    return tuple(map(int, iterable_content))


def to_cv_ref(x, frame_shape):
    return np.stack([x[..., 1], x[..., 0]], axis=-1)


def to_normal_ref(x, frame_shape):
    return np.stack([x[..., 1], frame_shape[0] - x[..., 0]], axis=-1)


class BoundingBox(BaseModel):
    top: float
    left: float
    bottom: float
    right: float
    color: Optional[Tuple[int, int, int]] = (0, 255, 0)
    extra_data: dict = {}


def draw_skeleton(
    image: np.ndarray, keypoints: np.ndarray, color, thickness: int
) -> np.ndarray:
    skeleton_format = [
        -2,
        0,
        0,
        1,
        2,
        [6, 7, 3],
        [8, 4],
        9,
        10,
        -1,
        -1,
        [5, 12, 13],
        [6, 14],
        15,
        16,
        -1,
        -1,
    ]

    for i, v in enumerate(skeleton_format):
        if v == -2:
            continue

        if any_nans(keypoints[i]):
            continue

        if v != -1:
            parents = v if isinstance(v, list) else [v]

            for p in parents:
                if any_nans(keypoints[p]):
                    continue

                image = cv2.line(
                    image,
                    to_int_tuple(keypoints[i]),
                    to_int_tuple(keypoints[p]),
                    color,
                    thickness=thickness,
                    lineType=cv2.LINE_AA,
                )

    return image


class BoundingBoxes(BaseModel):
    bboxes: Sequence[BoundingBox]

    async def view(self, image: QImage, out_path: str):
        cv2.imwrite(
            out_path,
            self.draw_bboxes(image.get()),
        )

    def draw_bboxes(self, image_buffer: np.ndarray) -> np.ndarray:
        for bbox in self.bboxes:
            image_buffer = cv2.rectangle(
                image_buffer,
                (int(bbox.top), int(bbox.left)),
                (int(bbox.bottom), int(bbox.right)),
                bbox.color,
                4,
            )

            if "kps" in bbox.extra_data:
                kps = bbox.extra_data["kps"]

                # Convert to the proper referential
                kps = to_cv_ref(kps, image_buffer.shape)

                image_buffer = draw_skeleton(image_buffer, kps, bbox.color, 4)

        return image_buffer


class BoundingBoxesSequences(BaseModel):
    bboxes: Sequence[BoundingBoxes]

    async def view(self, video: QVideo, out_path: str):
        await self.draw_bboxes(video, out_path)

    async def draw_bboxes(self, video: QVideo, out_path: str):
        try:
            from vidgear.gears import WriteGear
        except ImportError:
            raise ImportError("Please install vidgear with pip install vidgear")

        writer = WriteGear(
            output=out_path,
            compression_mode=True,
            **{
                "-input_framerate": int(video.fps),
            },
        )

        # Create a ThreadPoolExecutor to run writer.write in a separate thread
        executor = ThreadPoolExecutor(max_workers=1)

        currentIndex = 0

        async for _, item in video.video_feed():
            # Copy to draw on top of
            copied_frames = item.copy()

            # Use asyncio to run the blocking I/O operation in a separate thread
            for f in copied_frames:
                if currentIndex < len(self.bboxes):
                    frame = self.bboxes[currentIndex].draw_bboxes(f)
                else:
                    frame = f

                await asyncio.get_running_loop().run_in_executor(
                    executor, writer.write, frame
                )
                currentIndex += 1

        # Cleanup: close the writer and shutdown the executor
        writer.close()
        executor.shutdown()
