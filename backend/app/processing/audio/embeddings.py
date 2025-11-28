import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_audio_text(text: str) -> np.ndarray:
    emb = EMBED_MODEL.encode(text)
    return emb.astype(np.float32)               # tiny, fast, perfect for CPU storage
