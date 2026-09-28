# RootIQ

**Find the cause before it becomes an outage** — alert storm → one incident → evidence-backed RCA → engineer approve-only remediation in under 60 seconds.

![RootIQ demo](docs/deck/rootiq-demo.gif)

Venture X Hackathon — Infrastructure & Cloud · Mode: **sim-first** (live EVE-NG additive)

## Quick start (3 commands)

```powershell
# 1) Backend (sim)
cd backend; .\.venv\Scripts\Activate.ps1; $env:ROOTIQ_MODE='sim'; uvicorn app.main:app --host 127.0.0.1 --port 8000

# 2) Frontend (other terminal)
cd frontend; npm run dev

# 3) Open UI
start http://localhost:5173
```

API health: http://localhost:8000/api/health · UI: http://localhost:5173

## Architecture

Lab collector → FastAPI ingest → detect/correlate/RCA/explain → WebSocket UI → approve → whitelisted lab agent.

Full Mermaid + 30s verbal: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Modes

| | |
|---|---|
| `ROOTIQ_MODE=sim` | In-process simulator (default, offline, backup) |
| `ROOTIQ_MODE=live` | EVE-NG + COLLECTOR-01 + lab agent |

UI badge always shows the active mode.

## Measured results

From `GET /api/runs` (9 sim runs) — details in [`docs/RESULTS.md`](docs/RESULTS.md):

| Metric | Target | Measured |
|---|---|---|
| Time to RCA | &lt; 60 s | **12.3 s** |
| Top-1 root | Top 3 | **9/9** |
| Noise reduction | 30% | **96.3%** |
| Human approval | 100% | **100%** |

## Pitch & demo

- Deck: [`docs/RootIQ_Pitch_Deck_Final.pptx`](docs/RootIQ_Pitch_Deck_Final.pptx) (numbers from RESULTS)
- Script: [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md)
- Judge Q&A: [`docs/QA_BANK.md`](docs/QA_BANK.md)
- Rehearsal / drills: [`docs/REHEARSAL.md`](docs/REHEARSAL.md) · Bag: [`docs/BAG.md`](docs/BAG.md)
- Backup video checklist: [`docs/demo-backup.md`](docs/demo-backup.md)
- Ship tag: **`v1.0`**

## Demo hotkeys

Shift+1 uplink · Shift+2 DNS · Shift+3 server spike · Shift+R reset · Shift+P presenter

## Team

| Role | Who |
|---|---|
| FE / keyboard demo | Ahmed |
| BE / AI / INFRA / Presenter | Team (see kickoff) |

## Docs

Contracts · Architecture · Results · Progress (`docs/progress/`) · Full plan `RootIQ_Daily_Plan.md`

## Feature freeze

After Day 11 / `v1.0-rc1`: **no new features** — bugfixes only with two-person review.
