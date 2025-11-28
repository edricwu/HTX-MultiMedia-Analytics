# Media Analytics System — Video + Audio Intelligence Platform

A full-stack media analysis pipeline with:
- Video object detection + keyframe extraction  
- Audio transcription with timestamps + confidence  
- Embedding + FAISS semantic cross-media search  
- Frontend dashboard to browse, upload & search  
- Fully dockerized deployment

---

## Features Implemented

| Capability | Status |
|---|---|
| Upload/Process Video → Keyframes + Objects | ✅ |
| Upload/Process Audio → Whisper Transcription | ✅ |
| Generate Text Embeddings (MiniLM-L6-v2) | ✅ |
| Unified Media Vector Search (FAISS) | ✅ |
| View Video Frames with Bounding Boxes | ✅ |
| View Audio Segments + Confidence | ✅ |
| Cross-Type Search: text/video/audio → results | ✅ |
| Docker + Docker Compose Deployment | ✅ |
| Backend + Frontend Test Suites | ✅ |

---

## Technologies

| Component | Choice |
|---|---|
| Backend Framework | FastAPI |
| Database | SQLite |
| Video Model | MobileNet-SSD (OpenCV) |
| Audio Model | Whisper-tiny |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Search | FAISS (in-memory indexed) |
| Frontend | Next.js + Tailwind |
| Deployment | Docker + Compose |

---

## Architecture
Full version in ```architecture.pdf```

```
                    FRONTEND (Next.js)
                    ┌─────────────────────┐
                    │ Upload | Search UI  │
                    │ Audio  | Video View │
                    └─────────────▲───────┘
                                  │ REST
                                  ▼
───────────────────────────────────────────────────────────────
                    BACKEND (FastAPI)
                    ┌─────────────────────────────────────┐
  process/video  →  │ keyframes → objects → summary+embed │
  process/audio  →  │ whisper → segments → embed          │
                    │ SQLite store + FAISS index          │
  /videos          →│ list processed frames               │
  /transcriptions  →│ list audio transcripts              │
  /search          →│ cross-media semantic retrieval       │
                    └─────────────────────────────────────┘
───────────────────────────────────────────────────────────────
```

---

## Quick Start (Docker Compose)

Run both backend + frontend with ONE command:

```bash
docker compose up --build
```

Access UI:

- Frontend → http://localhost:3000  
- Backend API → http://localhost:8000  

---

## Run Without Docker (Dev Mode)

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/process/video` | Upload & analyze video |
| POST | `/process/audio` | Upload & transcribe audio |
| GET  | `/videos` | List processed videos |
| GET  | `/transcriptions` | List audio transcriptions |
| GET  | `/search?q=text` | Text semantic search |
| GET  | `/search?video_id=id` | Similar video search |
| GET  | `/search?audio_id=id` | Similar audio search |

Example:
```bash
curl "http://localhost:8000/search?q=car"
```

---

## Testing

### Backend Tests

Local:
```bash
pytest backend/tests -q
```

Docker:
```bash
docker compose run --rm backend-tests
```

Coverage:
- Keyframe extraction  
- Object detection  
- Whisper transcription  
- API response correctness  
- Cross-media FAISS semantic retrieval  

---

### Frontend Tests

Local:
```bash
cd frontend
npm test
```

Docker:
```bash
docker compose run --rm frontend-tests
```

Covers:
- Video/audio upload workflow  
- Unified search functionality  
- Bounding-box video view UI  
- Transcript + timestamps view  
- Cross-media visual/audio similarity search UI  

---

## Repository Structure

```
backend/
 ├ app/
 │ ├ processing/ (video+audio pipeline)
 | ├ database_ops/ (database operations)
 | ├ models_data/ (model files - MobileNet)
 │ ├ services/ (FAISS + queue)
 │ ├ routes/ (routing)
 │ ├ data/
 | ├ uploads/
 │ └ main.py
 ├ test/ (pytest cases)
 ├ requirements.txt
 └ Dockerfile
frontend/
 ├ pages/ (UI pages)
 ├ components/
 ├ __tests__/ (Jest + RTL)
 └ Dockerfile
docker-compose.yml
README.md   ← THIS FILE
```
