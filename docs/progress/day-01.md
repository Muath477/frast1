# Day 01 — Foundation

## Acceptance
- [x] `configs/topology.json` — 5 nodes · 4 links · 2 services
- [x] Vite + React Flow + Shell/Sidebar (7 items)
- [x] FastAPI `/api/health` → `{"status":"ok","mode":"sim"}`
- [x] `/api/topology` → `5 4`
- [x] Frontend build / `tsc` OK
- [x] `thresholds.py` + `test_thresholds.py` — **7 passed**
- [x] `docker-compose.yml` + `backend/Dockerfile` + `scripts/dev.sh` present
- [ ] `docker compose up -d db` healthy — Docker not installed on this machine
- [ ] EVE-NG 5 nodes + `lab/eve/rootiq.unl` — INFRA deferred (see `lab/eve/README.md`)
- [x] `git tag day-01` pushed

## AI
`backend/app/intelligence/thresholds.py` maps contract §2.4 (`up`/`down` severities). Extra metric `poll_timeout` added for collector timeouts (Day 4).

## Verify
```powershell
Invoke-RestMethod http://localhost:8000/api/health
cd backend; pytest -q tests/test_thresholds.py
cd frontend; npm run build
```
