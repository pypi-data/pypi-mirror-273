from typing import List, Optional

import numpy as np
import numpy.typing as npt
from scale_sensor_fusion_io.models.sensors.camera.camera_sensor import CameraSensor
from scale_sensor_fusion_io.utils.camera_helpers import global_to_local, project_distort


def compute_photocolors(
    positions: npt.NDArray[np.float32],
    cameras: List[CameraSensor],
    points_timestamps: Optional[npt.NDArray[np.uint32]],
    frame_timestamp: Optional[int],
) -> npt.NDArray[np.uint8]:
    """
    Compute photocolors for provided points.

    Photocolors are computed by projecting each point into each camera and
    sampling the color of the pixel that the point projects to.
    """
    # initialize color to shape of point position
    colors = np.full(positions.shape, 255, dtype=np.uint8)

    start_timestamp = (
        int(np.min(points_timestamps))
        if points_timestamps is not None
        else frame_timestamp
    )
    if start_timestamp is None:
        raise ValueError("Must provide either points_timestamps or frame_timestamp")

    # For each camera, find the frame that is closest to the point's timestamp
    for camera in cameras:
        image_data, content_timestamp = camera.get_closest_content_at_timestamp(
            start_timestamp
        )

        intrinsics = camera.intrinsics
        camera_pose = camera.poses.interpolate([content_timestamp]).values[0]

        local_points = global_to_local(
            positions,
            camera_pose,
        )
        x, y, mask = project_distort(local_points, intrinsics)

        mask = np.logical_and(
            mask,
            np.logical_and(
                np.logical_and(x >= 0, x < image_data.shape[1]),
                np.logical_and(y >= 0, y < image_data.shape[0]),
            ),
        )

        index = np.argwhere(mask).reshape(-1)
        pixels = np.array(np.vstack([x, y]).T[mask], dtype=np.int32)

        colors[index] = [image_data[pixels[:, 1], pixels[:, 0], :]]
    return colors
