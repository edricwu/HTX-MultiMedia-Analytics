import json
import os
from fastapi import APIRouter
from app.database import get_db

router = APIRouter()

@router.get("/transcriptions")
def get_transcriptions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, filename, transcript, segments_json, datetime(created_at, 'localtime') AS created_local FROM audio_transcriptions")
    rows = cur.fetchall()

    results = []

    for r in rows:
        # 🔥 Convert string->array thanks to json.loads()
        try:
            segments = json.loads(r["segments_json"])
        except Exception:
            segments = []   # fallback if corrupted

        results.append({
            "id": r["id"],
            "filename": os.path.basename(r["filename"]),
            "transcript": r["transcript"],
            "segments": segments,         # ← Now proper list
            "created_at": r["created_local"]
        })

    return results
