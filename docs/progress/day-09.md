# Day 09 — Wow moment (AlertStorm · MTTD · Noise Reduction · 3 scenarios)

## FE
- [x] AlertStorm: Traditional NMS vs RootIQ + Noise reduction %
- [x] MTTD Stopwatch: starts at inject, freezes at analyzedAt
- [x] Services panel with DNS dependency hint

## BE
- [x] `/api/runs` returns `{runs, summary}` with top1Accuracy / avgTimeToRootCause / avgNoiseReduction
- [x] Isolation Forest module ready (trains when healthy recording exists)

## Verify (sim)
| Scenario | Expected root | Hotkey |
|---|---|---|
| uplink-congestion | link-r1-sw1 | ⇧1 |
| dns-failure | svc-dns | ⇧2 |
| server-spike | app01 | ⇧3 |

## Remaining for live lab
- 3×3 live runs + soak 30m when EVE-NG is up
