from app.processing.video.keyframes import extract_keyframes
from app.processing.video.detection import detect_objects_on_frames
import os
import cv2

def test_detection_pipeline_runs():
    base_dir = os.path.dirname(__file__)
    video_path = os.path.abspath(
        os.path.join(base_dir, "..", "app", "data", "videos", "video_08.mp4")
    )

    frames = extract_keyframes(video_path)
    assert len(frames) > 0, "No keyframes extracted — video load failed?"

    detections = detect_objects_on_frames(frames)
    print(detections)

    assert isinstance(detections, list), "Detection output must be a list"
    assert "detections" in detections[0], "Missing detection structure"
