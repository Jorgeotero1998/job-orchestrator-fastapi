# Background Jobs Orchestrator — ES/EN

## Español

Plataforma para definir jobs y disparar ejecuciones (runs) usando **Celery + Redis**.

### Endpoints
- `/api/v1/jobs` (GET/POST)
- `/api/v1/jobs/{job_id}/runs` (POST)
- `/api/v1/jobs/runs` (GET)

### Worker
El repo incluye servicios `worker` y `beat` en `docker-compose.yml`.

---

## English

Background job orchestrator with Celery + Redis (API + worker + scheduler).

