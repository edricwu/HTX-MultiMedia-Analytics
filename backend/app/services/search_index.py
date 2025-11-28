# app/services/search_index.py

import faiss, json, re
import numpy as np
from sentence_transformers import SentenceTransformer
from app.database import get_db
import inflect       # convert numbers→words naturally


############################################
EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

MEDIA_INDEX = None
MEDIA_ITEMS = []    # <-- unchanged
INDEX_DIM = None

p = inflect.engine()   # number-word conversion


def filename_to_phrase(name: str) -> str:
    name = name.lower()
    name = re.sub(r'\.(mp4|mov|avi|mkv|wav|mp3)$', '', name)
    name = re.sub(r'[_\-]+', ' ', name)

    tokens = re.findall(r'[a-z]+|\d+', name)

    out = []
    for t in tokens:
        if t.isdigit():
            out.append(p.number_to_words(t))
        else:
            out.append(t)
    return " ".join(out)


def load_audio_records_for_faiss():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, filename, transcript, segments_json, embedding, created_at
        FROM audio_transcriptions
    """)
    rows = cur.fetchall()

    items = []
    for r in rows:
        stored_vec = np.frombuffer(r["embedding"], dtype=np.float32)

        # embed filename semantics too
        semantic_text = filename_to_phrase(r["filename"]) + " " + r["transcript"]
        semantic_vec = EMBED_MODEL.encode(semantic_text).astype(np.float32)

        combined = (stored_vec + semantic_vec) / 2

        items.append({
            "type": "audio",
            "id": r["id"],
            "filename": r["filename"],
            "transcript": r["transcript"],
            "segments_json": r["segments_json"],
            "embedding": combined,
            "created_at": r["created_at"]
        })

    return items

def load_video_records_for_faiss():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, filename, summary, objects_json, embedding, created_at
        FROM video_index
    """)
    rows = cur.fetchall()

    items = []
    for r in rows:
        stored_vec = np.frombuffer(r["embedding"], dtype=np.float32)

        # embed filename semantics too
        semantic_text = filename_to_phrase(r["filename"]) + " " + r["summary"]
        semantic_vec = EMBED_MODEL.encode(semantic_text).astype(np.float32)

        combined = (stored_vec + semantic_vec) / 2

        items.append({
            "type": "video",
            "id": r["id"],
            "filename": r["filename"],
            "summary": r["summary"],
            "objects_json": r["objects_json"],
            "embedding": combined,
            "created_at": r["created_at"]
        })

    return items

def rebuild_media_index():
    global MEDIA_INDEX, MEDIA_ITEMS, INDEX_DIM

    videos = load_video_records_for_faiss()
    audios = load_audio_records_for_faiss()

    MEDIA_ITEMS = videos + audios
    vectors = [item["embedding"] for item in MEDIA_ITEMS]

    if not vectors:
        MEDIA_INDEX = None
        return

    mat = np.stack(vectors).astype(np.float32)
    INDEX_DIM = mat.shape[1]

    faiss.normalize_L2(mat)
    index = faiss.IndexFlatIP(INDEX_DIM)
    index.add(mat)

    MEDIA_INDEX = index
    print(f"🔥 FAISS rebuilt with semantic filename mapping → {MEDIA_INDEX.ntotal} items")


############################################
def _ensure_index():
    if MEDIA_INDEX is None:
        rebuild_media_index()


############################################
# direct emb fetch unchanged
############################################
def get_video_embedding(video_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT embedding FROM video_index WHERE id = ?", (video_id,))
    row = cur.fetchone()
    return np.frombuffer(row[0], dtype=np.float32) if row else None


def get_audio_embedding(audio_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT embedding FROM audio_transcriptions WHERE id = ?", (audio_id,))
    row = cur.fetchone()
    return np.frombuffer(row[0], dtype=np.float32) if row else None
