# Day 13 — Final rehearsal & emergency drills

Stopwatch everything. Fill notes after each run. Script: `docs/DEMO_SCRIPT.md` · Q&A: `docs/QA_BANK.md`.

## Schedule

| Time | Activity | Owner | Done |
|---|---|---|---|
| 09:00 | Cold boot same laptop/screen/network + `./scripts/preflight.sh` | BE + FE | ☐ |
| 09:30 | Rehearsal 1 — Pitch + Demo + 2 Qs · stopwatch | ALL | ☐ |
| 10:30 | Fix notes from R1 (copy/order only — **no features**) | Presenter + FE | ☐ |
| 11:30 | Rehearsal 2 | ALL | ☐ |
| 13:30 | Emergency drills (below) — each &lt; 30s | ALL | ☐ |
| 15:30 | Rehearsal 3 — outsider as judge from `QA_BANK.md` | ALL | ☐ |
| 17:00 | Record backup video **v2** (OBS 1920×1080 ≤5:00) | Presenter | ☐ |
| 18:00 | Pack the bag (`docs/BAG.md`) | FE | ☐ |

## Rehearsal log

| # | Pitch+Demo (mm:ss) | ≤ limit? | Notes / fixes |
|---|---|---|---|
| 1 | __:__ | ☐ | |
| 2 | __:__ | ☐ | |
| 3 | __:__ | ☐ | |

Suggested limit: Pitch ≤ 2:00 + Demo ≤ 5:00 (per `DEMO_SCRIPT.md`).

## Emergency drills (muscle memory &lt; 30s)

| Fault | Response | Verified |
|---|---|---|
| EVE-NG hangs | «Let me switch to our recorded lab feed» → Settings **Use Simulation feed** (or TopBar badge) → continue; badge shows **SIMULATION** | ☐ API `POST /api/demo/mode {"mode":"sim"}` |
| Venue Wi‑Fi down | Do nothing — all local (`localhost`) | ☐ Day 11 offline path |
| Backend crash | `docker compose restart backend` (UI reconnects WS) | ☐ health probe |
| Laptop dies | Spare laptop (same repo + Docker + video) **or** play `docs/demo-backup.mp4` | ☐ bag |
| Judge wants other scenario | `Shift+R` then `Shift+2` (DNS) | ☐ `emergency_drills.py` |
| RCA looks wrong | Open CandidateRanking: «This is exactly why we show evidence and confidence instead of a black-box answer» → re-inject | ☐ candidates ≥2 |

Automate what you can:

```powershell
cd backend
.\.venv\Scripts\python.exe scripts\emergency_drills.py
```

## Release tag

Ship tag for the venue: **`v1.0`** (not just day tags).
