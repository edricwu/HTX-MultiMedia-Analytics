import numpy as np
from sentence_transformers import SentenceTransformer

VIDEO_EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_video_summary(text: str) -> np.ndarray:
    return VIDEO_EMBED_MODEL.encode(text).astype(np.float32)
