# app/services/queue.py

import time
import threading
import traceback
from queue import Queue
from uuid import uuid4

JOB_QUEUE = Queue()
JOB_STATUS = {}   # job_id → { type, file, status, progress, retries, error }

MAX_RETRIES = 3


# -------------- JOB SUBMISSION --------------
def submit_job(job_type: str, file_path: str) -> str:
    job_id = str(uuid4())

    JOB_STATUS[job_id] = {
        "type": job_type,      # "audio" / "video"
        "file": file_path,     # temp file path saved from upload
        "status": "queued",    # queued → running → complete / failed
        "progress": 0,         # % updated by pipeline functions
        "retries": MAX_RETRIES,
        "error": None
    }

    JOB_QUEUE.put(job_id)
    print(f"[PROCESS] Job submitted → {job_id} ({job_type})")

    return job_id


# -------------- WORKER LOOP ------------------
def worker():
    """
    Background worker that pulls tasks from JOB_QUEUE
    and executes audio/video pipeline flows.
    """

    # Lazy import to avoid circular import problems
    from app.processing.video.pipeline import process_video_file
    from app.processing.audio.pipeline import process_audio_file

    while True:
        job_id = JOB_QUEUE.get()
        job = JOB_STATUS[job_id]

        try:
            job["status"] = "running"
            start = time.time()
            print(f"[PROCESS] Running job {job_id} ({job['type']})")

            # ---------------- ROUTING -----------------
            if job["type"] == "video":
                process_video_file(job_id, job["file"])

            elif job["type"] == "audio":
                process_audio_file(job_id, job["file"])

            # ---------------- SUCCESS -----------------
            job["status"] = "complete"
            job["progress"] = 100
            print(f"[PROCESS] Job {job_id} completed in {time.time()-start:.2f}s")

        except Exception as e:
            job["retries"] -= 1
            job["error"] = str(e)
            job["status"] = "failed"

            print(f"[PROCESS] Job {job_id} failed: {e}")
            traceback.print_exc()

            if job["retries"] > 0:
                print(f"[PROCESS] Retrying {job_id} (remaining: {job['retries']})")
                JOB_QUEUE.put(job_id)
            else:
                print(f"[PROCESS] Job {job_id} permanently failed after max retries")

        finally:
            JOB_QUEUE.task_done()


# ----------------- START WORKER THREAD -----------------
worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()
print("[PROCESS] Background worker started")
