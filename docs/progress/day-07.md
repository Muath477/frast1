# Day 07 — Root Cause Analysis (M2)

## Acceptance
- [x] `rca.py` weights + suppression + confidence
- [x] `history.py` support / record
- [x] `test_rca.py` — **4 passed** (congestion / DNS / CPU / low-confidence)
- [x] Auto-analyze debounce ≤10s · map focus cause/impact · ConfidenceRing / candidates / evidence
- [x] sim inject uplink → `rootCause.entityId == link-r1-sw1`, confidence ≥ 0.8, analyze ≪ 60s
- [x] `pytest -q` — **31 passed**
- [x] `app.tools.replay` fallback
- [ ] `data/recordings` ≥ 10 live captures — INFRA deferred
- [x] Tags `day-07` · `m2`
