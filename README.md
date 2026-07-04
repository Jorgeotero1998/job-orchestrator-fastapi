# OteroJobs

**EN**: Background Job Orchestrator (API-first)  
**ES**: Orquestador de jobs (API-first)

## Live demo / Demo online
- **Web**: https://job-orchestrator-fastapi.vercel.app
- **API docs**: https://job-orchestrator-fastapi-api.onrender.com/docs
- **API health**: https://job-orchestrator-fastapi-api.onrender.com/api/v1/health

## Stack
- FastAPI
- PostgreSQL
- Docker
- Jobs
- AI (Groq)

## Local setup (Docker)

`ash
cp .env.example .env
docker compose up --build
`

## Credentials (demo)

**EN**: Default demo admin is seeded from ADMIN_EMAIL / ADMIN_PASSWORD.  
**ES**: El admin demo se crea desde ADMIN_EMAIL / ADMIN_PASSWORD.

## Deploy

**EN**:
- Backend: Render (Blueprint via ender.yaml)
- Frontend: Vercel (Root Directory: web)

**ES**:
- Backend: Render (Blueprint con ender.yaml)
- Frontend: Vercel (Root Directory: web)
