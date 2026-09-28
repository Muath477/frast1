# Day 11 — Hardening · Feature Freeze · v1.0-rc1

## Acceptance
- [x] Playwright `e2e/demo.spec.ts` ×3 full demo loops (sim) — **3 passed**
- [x] `data-testid`: root-cause · evidence-item · timeline · incident-status
- [x] Timeline `Rejected` via `timings.rejectedAt` (reject replaces pending action)
- [x] No second incident during `remediating`/`recovered` (E2E stability)
- [x] `frontend/Dockerfile` + `nginx.conf` · compose `frontend:8080`
- [x] `scripts/preflight.sh` · `scripts/demo-reset.sh`
- [x] README: EVE golden snapshot + boot order + freeze note
- [ ] Live ×3 consecutive · offline WiFi · `docker compose` / stats — INFRA/venue (Docker not on this host)
- [x] Tags `day-11` · `v1.0-rc1`

## Freeze
No new features after this tag — bugfixes only with 2-person review.
