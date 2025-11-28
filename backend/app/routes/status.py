
from fastapi import APIRouter
from app.services.queue import JOB_STATUS

router = APIRouter()

@router.get("/status/all")
def status_all():
    return JOB_STATUS

@router.get("/status/{job_id}")
def get_status(job_id: str):
    return JOB_STATUS.get(job_id, {"error": "job not found"})