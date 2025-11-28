import json
import numpy as np
from app.database import get_db
from app.processing.audio.embeddings import embed_audio_text   # or your function name
import app.services.search_index as si
import faiss


def save_audio_record(filename: str, transcript: str, segments: str):
    """
    Saves audio to SQLite and updates FAISS index incrementally (no rebuild needed).
    segments include timestamps + confidence scores.
    transcript is fed to MiniLM embedding model.
    """

    # ---- EMBEDDING (same embedding model as video) ----
    emb = embed_audio_text(transcript).astype(np.float32)
    emb_bytes = emb.tobytes()

    # ---- WRITE TO SQLITE ----
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO audio_transcriptions (filename, transcript, segments_json, embedding)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        transcript,
        json.dumps(segments),
        emb_bytes
    ))

    new_id = cur.lastrowid
    db.commit()

    # ---- 🔥 INCREMENTAL FAISS UPDATE ----
    try:
        if si.MEDIA_INDEX is not None and si.INDEX_DIM == emb.shape[0]:
            vec = emb.reshape(1, -1)
            faiss.normalize_L2(vec)

            # Append into shared index + metadata table
            si.MEDIA_ITEMS.append({
                "type": "audio",
                "id": new_id,
                "filename": filename,
                "transcript": transcript,
                "created_at": None,               # you can SELECT after insert if needed
                "embedding": emb
            })

            si.MEDIA_INDEX.add(vec)                  # O(1) insert ✔ fast
            print(f"[FAISS] index size = {si.MEDIA_INDEX.ntotal} vectors (dim={si.INDEX_DIM})")
            print(f"[FAISS] total media items tracked = {len(si.MEDIA_ITEMS)}")
            
        else:
            # If index not built, or dimension mismatch → rebuild full index
            print("FAISS index empty or dimension mismatch — rebuilding index.")
            from app.services.search_index import rebuild_media_index
            rebuild_media_index()

    except Exception as e:
        print(f"FAISS update failed, falling back to rebuild: {e}")
        from app.services.search_index import rebuild_media_index
        rebuild_media_index()

    return new_id
