from fastapi import FastAPI
from app.database import init_db

# === ROUTERS ===
from app.routes.process import router as process_router
from app.routes.status import router as status_router
# from app.routes.audio import router as audio_process_router
from app.routes.audio_read import router as audio_read_router
# from app.routes.video import router as video_process_router
from app.routes.video_read import router as video_read_router
from app.routes.search import router as search_router
from app.routes.stats import router as stats_router

app = FastAPI(title="Media Processing Backend")

@app.on_event("startup")
def startup():
    init_db()   # ensure tables exist


# ---------------- Register routes -------------------
app.include_router(process_router)
app.include_router(status_router)
app.include_router(audio_read_router)
app.include_router(video_read_router)
app.include_router(search_router)
app.include_router(stats_router)


@app.get("/health")
def health():
    return {"status": "ok"}
