import os
import cv2
import base64

from app.processing.video.keyframes import extract_keyframes
from app.processing.video.detection import detect_objects_on_frames
from app.processing.video.summary import build_video_summary
from app.database_ops.video import save_video_record
import app.services.queue as q

def process_video_file(job_id: str, file_path: str):
    status = q.JOB_STATUS[job_id]

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in {".mp4", ".mov", ".mkv", ".avi"}:
        raise ValueError(f"Unsupported video format: {ext}")
    
    status["progress"] = 10    # Stage 1: Keyframes
    frames = extract_keyframes(file_path)

    status["progress"] = 40    # Stage 2: Object detection
    detections = detect_objects_on_frames(frames)

    for f in detections:
        frame = f.pop("frame", None)
        if frame is None:
            continue

        # draw each bbox directly on frame
        for obj in f["detections"]:
            x1,y1,x2,y2 = obj["bbox"]

            # if model outputs normalized coords, scale here
            if max(x1,x2,y1,y2) <= 1.5:
                x1 *= frame.shape[1]; x2 *= frame.shape[1]
                y1 *= frame.shape[0]; y2 *= frame.shape[0]

            # draw rect + label
            cv2.rectangle(frame, (int(x1),int(y1)), (int(x2),int(y2)), (0,0,255), 2)
            label = f"{obj['object']} {obj['confidence']:.2f}"
            cv2.putText(frame, label, (int(x1),int(y1)-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

        # encode to base64 *after drawing boxes*
        _, buffer = cv2.imencode(".jpg", frame)
        f["frame_base64"] = base64.b64encode(buffer).decode("utf-8")

        # we already used frame — remove it to save DB space
        f["width"]  = frame.shape[1]
        f["height"] = frame.shape[0]

    status["progress"] = 70    # Stage 3: Summarize + embed
    summary = build_video_summary(detections)

    status["progress"] = 90    # Stage 4: DB save + FAISS update
    save_video_record(filename=file_path, detections=detections, summary=summary)

    status["progress"] = 100
    status["status"] = "complete"
    print(f"[PROCESS] Video job {job_id} finished.")
