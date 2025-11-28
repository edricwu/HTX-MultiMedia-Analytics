from fastapi import APIRouter, UploadFile
from app.processing.audio.transcribe import transcribe_audio
from app.database_ops.audio import save_audio_record

router = APIRouter(prefix="/process")

@router.post("/audio")
async def process_audio(file: UploadFile):
    path = f"app/data/audio/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = transcribe_audio(path)  # returns { "text", "segments" }

    save_audio_record(
        filename=file.filename,
        transcript=result["text"],
        segments=result["segments"]
    )

    return {
        "status": "ok",
        "filename": file.filename,
        "transcript": result["text"],
        "segments": result["segments"]
    }
