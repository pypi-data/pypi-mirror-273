import torch
import torch.nn.functional as F
import numpy as np


def resize_with_pad(image, target_height, target_width):
    batch_size, height, width, channels = image.shape

    # Compute the aspect ratio of the original image
    aspect_ratio = width / height

    # Compute the aspect ratio of the target size
    target_aspect_ratio = target_width / target_height

    # Calculate the size for resizing while maintaining aspect ratio
    if aspect_ratio > target_aspect_ratio:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    # Convert the image to PyTorch Tensor
    image = torch.from_numpy(image)

    # Reshape to (B,C,H,W)
    image = image.permute(0, 3, 1, 2)

    # Resize the image using the computed size
    resized_image = F.interpolate(image, size=(new_height, new_width), mode="nearest")

    # Calculate the amount of padding required
    pad_height = target_height - new_height
    pad_width = target_width - new_width
    pad_top = pad_height // 2
    pad_bottom = pad_height - pad_top
    pad_left = pad_width // 2
    pad_right = pad_width - pad_left

    # Pad the resized image
    padded_image = F.pad(resized_image, (pad_left, pad_right, pad_top, pad_bottom))

    # Reshape to (B,H,W,C)
    padded_image = padded_image.permute(0, 2, 3, 1).numpy()

    return padded_image


def resize_and_serialize(
    image, channel_first=False, input_size=[640, 640], tobytes=False, resize_info=False
):
    target_height, target_width = input_size
    image_height, image_width = image[0].shape[:2]
    if image_height > image_width:
        scale = target_height / image_height
        resized_height = target_height
        resized_width = int(image_width * scale)
    else:
        scale = target_width / image_width
        resized_height = int(image_height * scale)
        resized_width = target_width

    pad_h = target_height - resized_height
    pad_w = target_width - resized_width
    pad = (pad_h, pad_w)

    image_rs = resize_with_pad(image, target_height, target_width)

    if channel_first:
        image_rs = np.transpose(image_rs, [0, 3, 1, 2])  # HWC -> CHW
    # return image in bytes if requested

    if tobytes:
        packet = (image_rs.tobytes(), scale, pad, image)

    else:
        packet = (image_rs, scale, pad, image)

    if resize_info:
        return packet
    else:
        return packet[0]
