# RootIQ

Venture X Hackathon — Infrastructure & Cloud

**Demo day:** TBD (confirm in team kickoff)  
**Kickoff / Day 0:** 2026-09-28  
**Mode:** Simulator-first (small team). Live EVE-NG lab is additive.

**Promise:** From dozens of scattered alerts to one incident, evidence-backed root cause, and an action that executes only with engineer approval — in under 60 seconds.

## Roles
- FE: Ahmed
- BE / AI / INFRA / Presenter / Timekeeper: TBD

## Stack
- Frontend: Vite + React 19 + TypeScript + Tailwind CSS v4 + React Flow
- Backend: FastAPI + WebSocket (+ PostgreSQL when Docker available)
- Modes: `ROOTIQ_MODE=sim` (default) | `live`

## Quick start
```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (another terminal)
cd frontend
npm install
npm run dev
```

- API: http://localhost:8000/api/health
- UI: http://localhost:5173

## Docs
- Contracts (frozen): `docs/CONTRACTS.md`
- Daily rhythm: `docs/RHYTHM.md`
- Full plan: `RootIQ_Daily_Plan.md`
- Progress: `docs/progress/`

## Demo hotkeys
- Shift+1 uplink congestion · Shift+2 DNS failure · Shift+3 server spike · Shift+R reset · Shift+P presenter

## Docker (optional)
```bash
docker compose up -d --build
# UI http://localhost:8080  API http://localhost:8000
./scripts/preflight.sh
```

## E2E (sim)
```bash
# backend already on :8000 with ROOTIQ_MODE=sim
cd frontend && npx playwright install chromium
npm run test:e2e
```

## EVE-NG golden snapshot (when lab is healthy)
```bash
# On EVE host — stop nodes first, then:
# cp -a /opt/unetlab/tmp/0/<lab-uuid>/ /root/rootiq-golden/
# Restore: cp -a /root/rootiq-golden/. /opt/unetlab/tmp/0/<lab-uuid>/
```
**Boot order:** R1 → SW1/SW2 (wait ~90s) → APP-01 → COLLECTOR-01 → `systemctl status rootiq-collector rootiq-lab-agent`

## Feature freeze
After Day 11 / `v1.0-rc1`: no new features — fixes only, reviewed by two teammates.
