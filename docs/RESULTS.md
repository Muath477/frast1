# Measured results

Source of truth for the pitch deck. Regenerated from `GET /api/runs` after `python backend/scripts/day12_measure.py` (3 scenarios × 3 runs, `ROOTIQ_MODE=sim`).

> Live EVE ×9 fills the same table when the lab is available; until then **Measured in our lab (sim)** is what the deck cites.

## Deck table

| Metric | Deck target | Measured |
|---|---|---|
| Time to correlated RCA | &lt; 60 s | **12.3 s** avg (9 runs) |
| Root ranking | Top 3 | **Top-1 correct 9/9** |
| Alert noise reduction | 30% | **96.3%** avg |
| Human approval before remediation | 100% | **100%** (every run: reject + approve in Audit) |

## Summary from `/api/runs`

```json
{
  "count": 9,
  "top1Accuracy": 1.0,
  "avgTimeToRootCause": 12.317193984985352,
  "avgNoiseReduction": 0.9625706349844282
}
```

Rounded for slides: **~12 s** · **9/9** · **~96%** · **100%**.

## Per-run log (Day 12 measure)

| # | Scenario | Mode | Incident | TTD (s) | TTRCA (s) | Recover (s) | Raw alerts | Noise ↓ | Top-1 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | uplink-congestion | sim | INC-0001 | 0.56 | 10.60 | 27.12 | 33 | 97.0% | ✓ link-r1-sw1 |
| 2 | uplink-congestion | sim | INC-0002 | 0.50 | 10.78 | 27.52 | 33 | 97.0% | ✓ |
| 3 | uplink-congestion | sim | INC-0003 | 0.35 | 10.68 | 27.11 | 33 | 97.0% | ✓ |
| 4 | dns-failure | sim | INC-0004 | 0.49 | 11.62 | 27.66 | 29 | 96.6% | ✓ svc-dns |
| 5 | dns-failure | sim | INC-0005 | 0.20 | 10.53 | 26.11 | 26 | 96.2% | ✓ |
| 6 | dns-failure | sim | INC-0006 | 0.27 | 11.50 | 28.18 | 29 | 96.6% | ✓ |
| 7 | server-spike | sim | INC-0007 | 4.48 | 14.98 | 30.93 | 21 | 95.2% | ✓ app01 |
| 8 | server-spike | sim | INC-0008 | 4.52 | 15.12 | 31.42 | 22 | 95.5% | ✓ |
| 9 | server-spike | sim | INC-0009 | 4.51 | 15.05 | 32.01 | 22 | 95.5% | ✓ |

## Demo-script placeholders (uplink typical)

| Placeholder | Value |
|---|---|
| raw alerts (storm) | ~33 |
| time to root cause | ~11 s |
| noise reduction (story beat) | ~97% |
| top-1 across 9 runs | 9/9 |

## Human approval / audit

Every measured run executed: Reject (`Outside change window`) → Approve → Execute. Audit records `reject` and `approve`/`execute` before remediation. No auto-remediation path exists.

## Prior sim baselines (Day 9)

See earlier rows in git history / day-09 accept: top1=1.0, avg TTRCA≈12 s, noise≈98%. Consistent with Day 12.

## Tuning log

- Day 9: static threshold gate before z-score (false uplink during DNS/CPU).
- Day 9: Isolation Forest = supporting evidence only.
- Day 11: ignore anomalies while `remediating`/`recovered` (E2E stability).
- Day 12: nine-run measure script locked for deck numbers.
