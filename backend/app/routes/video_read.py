import os
import json
from fastapi import APIRouter
from app.database import get_db

router = APIRouter()

@router.get("/videos")
def list_videos():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, filename, summary, objects_json, datetime(created_at, 'localtime') AS created_local FROM video_index ORDER BY created_at DESC")
    rows = cur.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "filename": os.path.basename(r[1]),
            "summary": r[2],
            "detections": json.loads(r[3]),
            "created_at": r[4]
        })

    return results
