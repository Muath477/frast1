# Day 06 — Incidents (correlation + lifecycle + persistence)

## Acceptance
- [x] SQLAlchemy models (`incidents`, `evidence`, `actions`, `audit_log`, `runs`)
- [x] SQLite fallback when Postgres/Docker unavailable; dual-write JSON + DB
- [x] `Correlator` + `test_correlate.py`
- [x] `IncidentService` open/correlate/broadcast/archive
- [x] `GET /api/incidents` · IncidentPanel · Timeline · focus coloring
- [x] `IncidentsPage` table + status filter + detail panel
- [x] sim Shift+1 / inject → **1 open incident**, ≥3 members, rawAlerts ≥5
- [x] `pytest -q` — **31 passed**
- [x] `lab/collector/syslog_listener.py` (UDP 514 helper)
- [ ] Live syslog Gi0/1 flap — INFRA deferred
- [x] Tag `day-06`
