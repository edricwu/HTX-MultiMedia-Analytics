import os
from fastapi import APIRouter, UploadFile
from app.processing.video.keyframes import extract_keyframes
from app.processing.video.detection import detect_objects_on_frames   # already exists
from app.processing.video.summary import build_video_summary
from app.database_ops.video import save_video_record

router = APIRouter(prefix="/process")

@router.post("/video")
async def process_video(file: UploadFile):
    base_dir = os.path.dirname(__file__)
    path = os.path.abspath(
        os.path.join(base_dir, "..", "data", "videos", file.filename)
    )
    # path = f"app/data/videos/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    frames = extract_keyframes(path)
    detections = detect_objects_on_frames(frames) 

    summary = build_video_summary(detections)
    save_video_record(file.filename, detections, summary)

    return {
        "status": "ok",
        "filename": file.filename,
        "summary": summary,
        "detections": detections
    }
