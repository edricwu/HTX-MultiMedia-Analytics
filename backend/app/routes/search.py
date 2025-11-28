from fastapi import APIRouter, HTTPException
from typing import Optional
import numpy as np
import faiss
import os

import app.services.search_index as si

router = APIRouter()


@router.get("/search")
def unified_search(
    q: Optional[str] = None,
    video_id: Optional[int] = None,
    audio_id: Optional[int] = None,
    top_k: int = 10,
):
    """
    Unified search:
    - Text query:       /search?q=car
    - Visual similarity: /search?video_id=1
    - Audio similarity:  /search?audio_id=2
    """

    # validate: exactly one mode
    modes = [m is not None for m in (q, video_id, audio_id)]
    if sum(modes) != 1:
        raise HTTPException(
            status_code=400,
            detail="Provide exactly one of: q, video_id, audio_id",
        )

    si._ensure_index()
    if si.MEDIA_INDEX is None or not si.MEDIA_ITEMS:
        return []

    # 1) build query vector
    print("DEBUG q =", q, flush=True)
    if q is not None:
        # text query → embed
        query_vec = si.EMBED_MODEL.encode(q).astype(np.float32)
    elif video_id is not None:
        emb = si.get_video_embedding(video_id)
        if emb is None:
            raise HTTPException(status_code=404, detail="Video not found")
        query_vec = emb
    else:  # audio_id mode
        print(audio_id)
        emb = si.get_audio_embedding(audio_id)
        if emb is None:
            raise HTTPException(status_code=404, detail="Audio not found")
        query_vec = emb

    query_vec = query_vec.reshape(1, -1)
    faiss.normalize_L2(query_vec)

    # 2) search unified FAISS
    scores, idxs = si.MEDIA_INDEX.search(query_vec, top_k)
    idxs = idxs[0]
    scores = scores[0]

    results = []
    for score, idx in zip(scores, idxs):
        item = si.MEDIA_ITEMS[idx]
        # build clean response, don’t expose raw embedding
        base = {
            "type": item["type"],
            "id": item["id"],
            "filename": os.path.basename(item["filename"]),
            "score": float(score),
            "created_at": item["created_at"],
        }
        if item["type"] == "video":
            base["summary"] = item["summary"]
            base["objects_json"] = item["objects_json"]
        else:
            base["transcript"] = item["transcript"]
        results.append(base)

    return results
