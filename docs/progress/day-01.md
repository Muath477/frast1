# Day 01 — Foundation

## Acceptance
- [x] `configs/topology.json` — 5 nodes · 4 links · 2 services (single source of truth)
- [x] Vite + React + Tailwind + React Flow map
- [x] FastAPI `/api/health` → `{"status":"ok","mode":"sim"}`
- [x] `/api/topology` → 5 nodes / 4 links
- [x] Frontend `tsc` clean
- [x] `pytest tests/test_thresholds.py` — 7 passed
- [ ] Docker Postgres healthy — Docker not installed (sim OK)
- [ ] EVE-NG 5 nodes boot — INFRA later

## Verify commands
```powershell
Invoke-RestMethod http://localhost:8000/api/health
# topology nodes/links = 5 4
cd frontend; npm run build
cd backend; pytest -q tests/test_thresholds.py
```

## Note
`ifIndex` values are provisional — INFRA confirms via snmpwalk (Day 3/4 live).
