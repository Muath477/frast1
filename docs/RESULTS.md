# Results Log

| Run | Scenario | Mode | Root | Correct | Notes |
|---|---|---|---|---|---|
| sim-auto | uplink-congestion | sim | link-r1-sw1 | yes | pytest test_scenarios |
| sim-auto | dns-failure | sim | svc-dns | yes | after detector static-gate fix |
| sim-auto | server-spike | sim | app01 | yes | pytest test_scenarios |
| day9-accept | uplink-congestion | sim | link-r1-sw1 | yes | noise≈98.6% ttr≈10.6s |
| day9-accept | dns-failure | sim | svc-dns | yes | noise≈98.3% ttr≈12.1s |
| day9-accept | server-spike | sim | app01 | yes | noise≈97.1% ttr≈15.4s |

## Summary (sim Day 9)
- `top1Accuracy = 1.0`
- `avgTimeToRootCause ≈ 12s` (&lt; 60)
- `avgNoiseReduction ≈ 0.98`

## Tuning log
- Day 9: Detector requires static threshold cross before z-score can raise severity (prevents false link anomalies during DNS/CPU scenarios from tight EWMA).
- Day 9: Multivariate Isolation Forest is optional supporting evidence only (never selects root).
