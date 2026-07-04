from __future__ import annotations

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.api.v1.deps import get_current_user, get_db
from app.db.models.jobs import JobDefinition, JobRun
from app.workers.tasks import run_job

router = APIRouter()


class JobCreate(BaseModel):
    name: str
    description: str = ""


class JobOut(BaseModel):
    id: str
    name: str
    description: str


class RunCreate(BaseModel):
    input: dict = {}


class RunOut(BaseModel):
    id: str
    job_id: str
    status: str


@router.get("/jobs", response_model=list[JobOut])
async def list_jobs(db=Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(JobDefinition).order_by(JobDefinition.created_at.desc()))
    rows = result.scalars().all()
    return [JobOut(id=str(j.id), name=j.name, description=j.description) for j in rows]


@router.post("/jobs", response_model=JobOut)
async def create_job(payload: JobCreate, db=Depends(get_db), _=Depends(get_current_user)):
    job = JobDefinition(name=payload.name, description=payload.description)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return JobOut(id=str(job.id), name=job.name, description=job.description)


@router.post("/jobs/{job_id}/runs", response_model=RunOut)
async def create_run(job_id: str, payload: RunCreate, db=Depends(get_db), _=Depends(get_current_user)):
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job_id")

    result = await db.execute(select(JobDefinition).where(JobDefinition.id == job_uuid))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    run = JobRun(job_id=job_uuid, status="queued", input_json=json.dumps(payload.input or {}))
    db.add(run)
    await db.commit()
    await db.refresh(run)

    run_job.delay(str(run.id))  # background task (demo)
    return RunOut(id=str(run.id), job_id=str(run.job_id), status=run.status)


@router.get("/jobs/runs", response_model=list[RunOut])
async def list_runs(db=Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(JobRun).order_by(JobRun.created_at.desc()))
    rows = result.scalars().all()
    return [RunOut(id=str(r.id), job_id=str(r.job_id), status=r.status) for r in rows]

