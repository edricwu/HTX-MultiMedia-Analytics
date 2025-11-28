import json
import numpy as np
import faiss
from app.database import get_db
from app.processing.video.embeddings import embed_video_summary
import app.services.search_index as si


def save_video_record(filename: str, detections: list, summary: str):
    """
    Save processed video results into SQLite and incrementally update FAISS search index.
    detections: list of detected objects (with timestamps + counts)
    summary: string-based summary fed into MiniLM for embedding
    """

    # ---- EMBEDDING ----
    emb = embed_video_summary(summary).astype(np.float32)   # MiniLM vector
    emb_bytes = emb.tobytes()

    # ---- SQLite insert ----
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO video_index (filename, summary, objects_json, embedding)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        summary,
        json.dumps(detections),
        emb_bytes
    ))

    new_id = cur.lastrowid
    db.commit()

    # ---- 🔥 Incremental FAISS Update ----
    try:
        if si.MEDIA_INDEX is not None and si.INDEX_DIM == emb.shape[0]:
            vec = emb.reshape(1, -1)
            faiss.normalize_L2(vec)                 # required for inner-product = cosine

            si.MEDIA_ITEMS.append({
                "type": "video",
                "id": new_id,
                "filename": filename,
                "summary": summary,
                "objects_json": detections,
                "created_at": None,                 # you can fetch timestamp if needed
                "embedding": emb
            })

            si.MEDIA_INDEX.add(vec)                    # O(1) add → FAST
            print(f"[FAISS] index size = {si.MEDIA_INDEX.ntotal} vectors (dim={si.INDEX_DIM})")
            print(f"[FAISS] total media items tracked = {len(si.MEDIA_ITEMS)}")

        else:
            # Fallback — rebuild only if needed
            print("FAISS index missing or dimension mismatch — rebuilding index.")
            from app.services.search_index import rebuild_media_index
            rebuild_media_index()

    except Exception as e:
        print(f"Incremental FAISS update failed: {e}")
        from app.services.search_index import rebuild_media_index
        rebuild_media_index()

    return new_id
