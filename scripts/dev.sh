#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d db 2>/dev/null || true
( cd backend && source .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate; uvicorn app.main:app --reload --port 8000 ) &
( cd frontend && npm run dev ) &
wait
