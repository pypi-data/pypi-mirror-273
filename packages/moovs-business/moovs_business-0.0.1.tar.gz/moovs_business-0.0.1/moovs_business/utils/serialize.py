import numpy as np
from typing import List, Tuple
import torchvision.transforms as T

DESC_SIZE = (256, 128)


def arranging_pose_inputs(inputs):
    """Arrange the pose inputs to the correct order."""
    ids0, ids1, data, ms, info = zip(*inputs)

    ids = list(zip(ids0, ids1))

    data = np.stack(data, axis=0)

    return data, ids, ms, info


def preprocess(resize: bool = True, size: Tuple[int, int] = DESC_SIZE):
    # transformation
    transforms = []
    # Build transform functions
    transforms += [T.ToPILImage(mode="RGB")]
    if resize:
        transforms += [T.Resize(DESC_SIZE)]
    return T.Compose(transforms)


preprocess_func = preprocess()


def descriptor_preprocess_and_serialize(
    context_ref: List[np.ndarray],
    size: Tuple[int, int],
    tobytes: bool = True,
    channel_first: bool = True,
):
    """Preprocess and serialize the descriptor inputs."""
    im_batch = np.stack(
        [np.asarray(preprocess_func((ref[0])[2])) for ref in context_ref]
    )

    if channel_first:
        im_batch = np.transpose(im_batch, axes=(0, 3, 1, 2))

    # Return
    if tobytes:
        return im_batch.tobytes()
    else:
        return im_batch
