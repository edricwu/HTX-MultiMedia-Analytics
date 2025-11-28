# app/routes/process.py

from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import os
from app.services.queue import submit_job

router = APIRouter(prefix="/process")

TEMP_DIR = Path("app/uploads")
TEMP_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/video")
async def process_video(file: UploadFile = File(...)):
    filepath = TEMP_DIR / file.filename
    with open(filepath, "wb") as out:
        out.write(await file.read())

    job_id = submit_job("video", str(filepath))
    return {"job_id": job_id, "status": "queued"}


@router.post("/audio")
async def process_audio(file: UploadFile = File(...)):
    filepath = TEMP_DIR / file.filename
    with open(filepath, "wb") as out:
        out.write(await file.read())

    job_id = submit_job("audio", str(filepath))
    return {"job_id": job_id, "status": "queued"}
