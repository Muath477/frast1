# Day 08 — Approve / Reject / Recover (M3)

## Done (sim)
- [x] Action recommendations after RCA
- [x] Reject requires reason ≥ 5 chars → 422 otherwise
- [x] Approve → `simulator.remediate()` → recovery monitor → `resolved`
- [x] Audit log + ActionCard / RejectDialog / Settings engineer name
- [ ] Screen recording `m3.mp4` (team demo slot)
- [ ] Tag `day-08` / `m3` via PR (no direct main push)

## Demo script (5 min)
1. Shift+1 inject uplink congestion
2. Watch AlertStorm + incident + RCA (~12s)
3. Reject with reason → audit entry, still awaiting approval
4. Approve → remediating → recovered
5. Show timings on incident + `/api/runs`
