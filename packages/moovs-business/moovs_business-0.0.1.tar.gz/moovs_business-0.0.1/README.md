# moovs-business

`moovs-business` is a powerful Python package that empowers software with advanced capabilities in object detection, human pose estimation, and real-time multi-object tracking. This package is designed to revolutionize how applications interact with the physical world by providing easy-to-integrate tools for analyzing video content.

## Features

- **Object Detection**: Detect objects with precision focusing on people.
- **Multi-Object Tracking**: Track multiple objects over time in a video stream.
- **Human Pose Estimation**: Analyze human figures to estimate body poses.

## Installation

To use `moovs-business`, you will need Python 3.7 or later. Install the package using pip:

```bash
pip install moovs_business
```

## Configuration

Before you begin, ensure you have a valid `MOOVS_BUSINESS_API_KEY` configured in your environment variables. This is necessary for making requests to the remote services provided by the package.

## Usage

The package is designed to be used asynchronously. Here are some example scripts for each of the main features:

### Object Detection

```python
from moovs_business import DetectionFlow, QVideo
import asyncio

async def main():
    detector = DetectionFlow()
    video = QVideo("assets/surfing.mp4")
    bbox_sequence = await detector(video)
    await bbox_sequence.view(video, "output.mp4")

asyncio.run(main())
```

### Multi-Object Tracking

```python
from moovs_business import TrackingFlow, QVideo
import asyncio

async def main():
    tracking = TrackingFlow()
    video = QVideo("assets/simple-crowd.mp4")
    track_data = await tracking(video)
    await track_data.view(video, "output.mp4")

asyncio.run(main())
```

### Human Pose Estimation

```python
import asyncio
from moovs_business import PoseFlow, QVideo

async def main():
    pose_estimator = PoseFlow()
    video = QVideo("assets/surfing.mp4")
    pose_data = await pose_estimator(video)
    await pose_data.view(video, "surfing_ai.mp4")

asyncio.run(main())
```

## Contributing

Contributions are welcome! Feel free to open a pull request or an issue if you have suggestions or need help.
