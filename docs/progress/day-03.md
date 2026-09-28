# Day 03 — Live data path (Event → State → WS → Map)

## Acceptance
- [x] Schemas (`CamelModel`, `Event`) · Hub · StateStore (1Hz flush)
- [x] Pipeline ingest + port→link remap · `POST /events` 202 / 401 / 422
- [x] WS `/ws/operations` · snapshot · link/node/service broadcast
- [x] Simulator (`collectors/simulator.py`) baseline noise in `ROOTIQ_MODE=sim`
- [x] FE `ws.ts` · `useOps` · `useOpsSocket` · TopBar indicator · LinkInspector sparklines
- [x] Baseline EWMA + `test_baseline.py`
- [x] Manual event `r1/Gi0/0` → `link-r1-sw1` history shows ≥90 util
- [x] `pytest -q` — **31 passed**
- [x] `lab/app01/` setup refs (bind/nginx)
- [ ] Live dig/curl/iperf on APP-01 — INFRA deferred (no EVE)
- [x] Tag `day-03`
