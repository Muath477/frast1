# Results Log

| Run | Scenario | Mode | Root | Correct | Notes |
|---|---|---|---|---|---|
| sim-auto | uplink-congestion | sim | link-r1-sw1 | yes | pytest test_scenarios |
| sim-auto | dns-failure | sim | svc-dns | yes | after detector static-gate fix |
| sim-auto | server-spike | sim | app01 | yes | pytest test_scenarios |

## Tuning log
- Day 9: Detector now requires static threshold cross before z-score can raise severity (prevents false link anomalies during DNS/CPU scenarios from tight EWMA).
