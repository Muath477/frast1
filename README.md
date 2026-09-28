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
- Shift+1 uplink congestion · Shift+2 DNS failure · Shift+3 server spike · Shift+R reset
