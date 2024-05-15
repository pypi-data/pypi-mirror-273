import numpy as np
import cv2
from collections import OrderedDict


def resize_image(img, scale, bbox_center, output_shape):
    height, width = output_shape[:2]
    # Destination points are the corners of the output image
    dst_pts = np.float32(
        [[0, 0], [0, height - 1], [width - 1, height - 1], [width - 1, 0]]
    )

    # Calculate the points where the corners of the bounding box will be after scaling
    half_width_scaled = width * scale / 2
    half_height_scaled = height * scale / 2
    src_pts = np.float32(
        [
            [bbox_center[0] - half_width_scaled, bbox_center[1] - half_height_scaled],
            [bbox_center[0] - half_width_scaled, bbox_center[1] + half_height_scaled],
            [bbox_center[0] + half_width_scaled, bbox_center[1] + half_height_scaled],
            [bbox_center[0] + half_width_scaled, bbox_center[1] - half_height_scaled],
        ]
    )

    # Get the projective transform
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # Perform the transformation
    img_transformed = cv2.warpPerspective(
        img,
        M,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )

    # Transform for keypoints
    alpha = 1 / scale
    rx_xy = (1 - alpha) * bbox_center[0]
    ry_xy = (1 - alpha) * bbox_center[1]
    transform_xy = np.array([[alpha, 0.0], [0.0, alpha]], dtype=np.float32)
    tx_xy = bbox_center[0] - output_shape[1] / 2
    ty_xy = bbox_center[1] - output_shape[0] / 2
    M_keypoints = np.concatenate(
        [transform_xy, np.array([[rx_xy - tx_xy], [ry_xy - ty_xy]])], axis=1
    )

    return img_transformed, M_keypoints


def center_and_crop_image(img, bbox, output_shape=[384, 288, 3], context_scale=2.5):
    """_summary_

    Args:
        img (_type_): original image.
        bbox (_type_): _description_
        output_shape (list, optional): _description_. Defaults to [384, 288, 3].
        context_scale (float, optional): _description_. Defaults to 2.5.

    Returns:
        _type_: _description_
    """
    left, top, right, bottom = bbox

    y = bottom
    x = left
    w = right - left
    h = top - bottom
    center = np.array([x + w / 2.0, y + h / 2.0], dtype=np.float32)

    # input_shape = img.shape
    aspect_ratio = output_shape[1] / output_shape[0]

    if w > aspect_ratio * h:
        h = w / aspect_ratio
    scale = (h * context_scale) / output_shape[0]

    resized_img, M = resize_image(img, scale, center, output_shape[:2])
    cropped_img = img[int(top) : int(bottom), int(left) : int(right)]

    return resized_img, M, cropped_img


def extract_crops(inputs, output_shape=[384, 288], context_scale=2.0):
    """_summary_

    Args:
        x : List[frame,[Predictions]]:
    Returns:
        _type_: Returns a list with tuples according to Batching Requirements
        [(data, batch_id), (data, batch_id), ...]
        data=[(imcrop,(x1,x2,y1,y2),score,class),...]
    """
    output_shape = [*output_shape, 3]
    ref_frames, values = inputs
    frames = ref_frames
    # ensure np.int type

    outputs = []
    p_count = len(values)

    for index in range(p_count):
        frame = frames[index]
        frame_shape = frame.shape

        if values[index] is None:
            outputs.append(
                (
                    None,
                    index,
                )
            )

        else:
            bboxs = values[index][:, 0:4]
            scores = values[index][:, 4]
            classes = values[index][:, 5]
            # add none if no box detected for that frame

            for i, bbox in enumerate(bboxs):
                # extract bbox | cast to int
                bbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]

                # crop and add to the list & increase the image
                im_crop_evopose, M, img_crop_descriptor = center_and_crop_image(
                    frame, bbox, output_shape=output_shape, context_scale=context_scale
                )

                outputs.append(
                    (
                        (
                            im_crop_evopose,  # img crop for evopose
                            M,  # crop properties
                            img_crop_descriptor,  # im crop for descriptor
                            bbox,  # bbox
                            scores[i],  # score
                            classes[i],  # class_id
                            frame_shape,  # frame shape
                        ),
                        index,
                    )
                )
    return outputs


def scale_bounding_box_predictions(bboxs, scale, pad, frame_shape):
    outputs = []
    (pad_h, pad_w) = pad
    frame_area = frame_shape[0] * frame_shape[1]
    const = np.array([[pad_w / 2, pad_h / 2, pad_w / 2, pad_h / 2]], dtype=np.float32)

    # multiply elements from tuple frame shape
    for i in range(len(bboxs)):
        if len(bboxs[i]):
            tmp = np.array(bboxs[i], dtype=np.float32)
            tmp[:, 0:4] = (tmp[:, 0:4] - const) / scale
            # min of tmp is 0
            tmp[:, 0:4] = np.maximum(tmp[:, 0:4], 0)
            # calculate area of bbox
            bbox_area = (tmp[:, 2] - tmp[:, 0]) * (tmp[:, 3] - tmp[:, 1])
            # if bbox area > 90% of frame area, then remove bbox
            # since the object detection model is on the cluster, it is not able to know the maximum frame shape
            filter_out = np.logical_and(bbox_area < 0.9 * frame_area, bbox_area > 0.0)
            tmp = tmp[filter_out] if np.any(filter_out) else None
            # append tmp
            outputs.append(tmp)
        else:
            outputs.append(None)

    # print([len(tmp) for tmp in outputs],"-------------------")
    return outputs


def scale_pose_predictions(data, outputs, kwargs):
    # img = data[0]
    info = data[3]
    Ms = np.array(data[2], dtype=np.float32)
    keypoint_coords = np.array(outputs[0], dtype=np.float32)
    keypoint_scores = np.array(outputs[1], dtype=np.float32)

    S, b = Ms[:, :, :2], Ms[:, :, 2:]
    S_inv = np.linalg.inv(S)
    Sip = np.einsum("bik, bjk -> bji", S_inv, keypoint_coords[:, :, :2])
    bias = np.einsum("bik, bku -> bui", S_inv, b)
    keypoint_coords = Sip - bias

    keypoint_coords = np.flip(keypoint_coords, axis=-1)

    outputs = (keypoint_coords, keypoint_scores)

    kwargs = kwargs[0]

    outputs = [
        (*kw_i, o0_i, o1_i, info_i)
        for kw_i, o0_i, o1_i, info_i in zip(kwargs, outputs[0], outputs[1], info)
    ]

    return outputs


def sort_within_batch(outputs):
    """Order the returned instances produced by a remote call and aggregated by Join Class.

    Args:
        outputs (dict): The outputs. Contains every instance of the batch.
        Each instance contains its own results Tuple with.
        If no result is returned - output = None
        (Key ID, [remote outputs])
        Key ID - (Object Ref (original image), batch id)
    """
    # for each batch idx, add
    ordered_dict = {}

    for key, value in outputs.items():
        if key == "count":
            continue
        ref = value[0]
        if ref is not None:
            ray_image_ref, batch_id = ref
            features = value[1]
            # img crop | crop properties | bbox | score | class_id | frame_shape
            (
                imcrop_evopose,
                crop_properties,
                imcrop_descriptor,
                bbox,
                score,
                class_id,
                frame_shape,
            ) = ray_image_ref
            if batch_id not in ordered_dict:
                ordered_dict[batch_id] = [
                    (
                        bbox,
                        score,
                        class_id,
                        frame_shape,
                        features,
                        (imcrop_descriptor),
                        (imcrop_evopose),
                        (crop_properties),
                    )
                ]
            else:
                ordered_dict[batch_id].append(
                    (
                        bbox,
                        score,
                        class_id,
                        frame_shape,
                        features,
                        (imcrop_descriptor),
                        (imcrop_evopose),
                        (crop_properties),
                    )
                )
        else:
            batch_id = value[1]
            ordered_dict[batch_id] = None

    # order the dict
    od = OrderedDict(sorted(ordered_dict.items()))
    # get the ordered values
    values = list(od.values())
    # return values
    return values
