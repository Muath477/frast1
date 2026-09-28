# Day 09 — Scenarios 2/3 + Wow moment

## Acceptance
- [x] AlertStorm (NMS vs RootIQ + Noise reduction)
- [x] MttdStopwatch (freeze at analyzedAt · target &lt; 60s)
- [x] Services panel DNS dependency hint
- [x] Incident panel Network / DNS / Server icons
- [x] `anomaly.py` Isolation Forest + analyze evidence when score &gt; 0.6
- [x] `GET /api/runs` summary · `EXPECTED_ROOT` for `correct`
- [x] sim 3 scenarios reject→approve→recover — **DAY9_OK**
  - uplink → `link-r1-sw1` · dns → `svc-dns` · cpu → `app01`
  - `top1Accuracy=1.0` · `avgTimeToRootCause≈12s` · noise ≥ 80%
- [x] `pytest` scenarios + rca green
- [ ] Live 3×3 + 30m soak — INFRA deferred (no EVE)
- [x] Tag `day-09`
