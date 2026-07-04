from __future__ import annotations

import time

from app.core.logging import get_logger
from app.workers.celery_app import celery_app

log = get_logger(__name__)


@celery_app.task(name="app.workers.tasks.heartbeat")
def heartbeat():
    log.info("celery_heartbeat")
    return {"status": "ok"}


@celery_app.task(name="app.workers.tasks.run_job")
def run_job(run_id: str):
    # demo task: in a real system you'd update DB status and store logs.
    log.info("job_started", run_id=run_id)
    time.sleep(1)
    log.info("job_finished", run_id=run_id)
    return {"run_id": run_id, "status": "finished"}

