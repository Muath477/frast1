# Day 08 — Action / approval / recovery (M3)

## Acceptance
- [x] `action_service` recommendations · approve / reject (≥5 chars → else 422)
- [x] Reject audits + replacement pending action (lab not called)
- [x] Approve → sim `remediate` / live lab agent · `executed`
- [x] Recovery monitor → `resolved` + timings + `runs` metrics (`correct=True`)
- [x] `explain.py` grounded templates · `test_explain.py` **3 passed**
- [x] ActionCard · RejectDialog · AuditPage · Settings engineer
- [x] Timeline milestones (Injected→Recovered) · KPI MTTD/MTTR · edge stroke 1.2s
- [x] sim full loop: reject → approve → recover ≤45s — **M3_OK**
- [x] `pytest -q` **31** · `npm test` **2**
- [ ] Live QoS on R1 / `m3.mp4` — INFRA deferred
- [x] Tags `day-08` · `m3`
