import cv2
import numpy as np

def extract_keyframes(video_path, hist_thresh=0.15, min_valid_frames=1):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file {video_path}")

    keyframes = []
    frame_index = 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    prev_hist = None
    valid_frames = 0

    while True:
        ret, frame = cap.read()

        # CASE 1: No more frames → stop normally
        if not ret:
            break

        # CASE 2: Frame is None → corrupted video OR audio disguised
        if frame is None:
            cap.release()
            raise ValueError(f"Decoded frame is None — likely not a true video or file is corrupted: {video_path}")

        valid_frames += 1

        # CASE 3: No valid frames extracted at all
        if valid_frames == 1:
            # proceed but mark success only if we get >1
            pass

        # Convert to HSV → brightness + color shifts included
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0,1], None, [50,60], [0,180,0,256])
        hist = cv2.normalize(hist, hist).flatten()

        if prev_hist is None:
            keyframes.append({"frame_index": frame_index, "timestamp": frame_index / fps, "frame": frame})
        else:
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
            if diff > hist_thresh:
                keyframes.append({"frame_index": frame_index, "timestamp": frame_index / fps, "frame": frame})

        prev_hist = hist
        frame_index += 1

    cap.release()

    # FINAL VALIDATION
    if valid_frames < min_valid_frames:
        raise ValueError(f"No valid video frames found — File is corrupted or audio-only: {video_path}")

    return keyframes
