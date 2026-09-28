# Compressed plans (Appendix د)

Only use if the full 14-day path slips. Full path is already tagged through **`v1.0`** — keep this for future hackathons / restarts.

## 7-day compression

| Day | Maps to full plan | Drop |
|---|---|---|
| 1 | 0 + 1 + 2 | — |
| 2 | 3 + 4 | Devices page, Syslog |
| 3 | 5 + 6 | DB persistence (keep memory + JSON) |
| 4 | 7 | Recorder / Replay |
| 5 | 8 + 9 (DNS as **only** second scenario) | Isolation Forest, CPU scenario |
| 6 | 11 + 12 | Arabic, Replay, Analytics (table enough) |
| 7 | 13 + 14 | — |

## 48-hour on-site hackathon

| Hours | Task |
|---|---|
| 0–4 | Repo + `topology.json` + React Flow with ports + FastAPI + Simulator |
| 4–10 | WS + Store + inject (sim) + raw alerts |
| 10–16 | Detector + Correlator + RCA + incident panel |
| 16–22 | Approve/Reject + Recovery + Timeline + AlertStorm + Stopwatch |
| 22–28 | **Mandatory 6 h sleep** (rotating) |
| 28–36 | Live lab (if pre-staged) + collector + **one** live scenario |
| 36–42 | Harden + Playwright + backup video |
| 42–48 | Deck with measured numbers + 3 rehearsals |

> For 48 h: stage a **full EVE-NG lab before** the event if rules allow.
