import os 
from app.processing.audio.transcribe import transcribe_audio
from app.database_ops.audio import save_audio_record
import app.services.queue as q

def process_audio_file(job_id: str, file_path: str):
    status = q.JOB_STATUS[job_id]

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg"}:
        raise ValueError(f"Unsupported audio format: {ext}")

    status["progress"] = 20    # Stage 1: Whisper transcription
    result = transcribe_audio(file_path)

    status["progress"] = 70    # Stage 2: embedding + DB write
    save_audio_record(
        filename=file_path,
        transcript=result["text"],
        segments=result["segments"]
    )

    status["progress"] = 100
    status["status"] = "complete"
    print(f"[PROCESS] Audio job {job_id} finished.")
