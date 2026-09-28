# Day 10 — Differentiation (Arabic · Replay · Analytics · Presenter)

## Acceptance
- [x] i18n EN/AR + RTL dir flip · TopBar language toggle
- [x] IBM Plex Sans Arabic `@font-face` (drop woff2 into `frontend/public/fonts/`)
- [x] Explanation uses `explanation.ar` when lang=ar · `<bdi>` for IDs
- [x] `GET /api/incidents/{id}/replay` + IncidentReplay 5×
- [x] AnalyticsPage from `/api/runs` + BarChart + Target=60s
- [x] Presenter mode `Shift+P` (hide sidebar, 115%, idle cursor)
- [x] Empty healthy banner · ErrorBoundary Reconnecting · tab title `● N incident`
- [x] Hot `POST /api/demo/mode` (pause/resume sim + reset + snapshot)
- [x] Events rate-limit 50/s + timestamp skew ≤5m
- [ ] RTL screenshot pack in `docs/progress/rtl/` — optional at venue
- [x] Tag `day-10`
