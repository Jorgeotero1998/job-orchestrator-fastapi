from __future__ import annotations

import time

from app.core.logging import get_logger

log = get_logger(__name__)


def run_job_inline(run_id: str) -> None:
    log.info("job_started", run_id=run_id, mode="inline")
    time.sleep(1)
    log.info("job_finished", run_id=run_id, mode="inline")

