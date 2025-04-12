from fastapi import FastAPI, BackgroundTasks
from main import process_job_link
from pydantic import BaseModel
from typing import List
import uuid
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JOB_STATUS = {}

class JobInput(BaseModel):
    url: str

@app.post("/submit")
def submit_job(job: JobInput, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    JOB_STATUS[job_id] = {"url": job.url, "status": "Processing..."}
    background_tasks.add_task(process_job_link, job.url, job_id, JOB_STATUS)
    return {"job_id": job_id}

@app.get("/status")
def get_status():
    return JOB_STATUS
