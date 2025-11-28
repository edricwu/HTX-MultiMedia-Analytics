# app/routes/stats.py

from fastapi import APIRouter
import app.services.search_index as si

router = APIRouter()

@router.get("/stats/faiss")
def faiss_stats():
    if si.MEDIA_INDEX is None:
        return {"status": "empty"}

    return {
        "vectors": si.MEDIA_INDEX.ntotal,
        "dimension": si.INDEX_DIM,
        "media_items": len(si.MEDIA_ITEMS),
        "videos": len([m for m in si.MEDIA_ITEMS if m["type"] == "video"]),
        "audios": len([m for m in si.MEDIA_ITEMS if m["type"] == "audio"])
    }
