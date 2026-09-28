# Daily rhythm (fixed)

| Time | Activity | Output |
|---|---|---|
| 09:00–09:15 | Standup: yesterday / today / blockers | Task board update |
| 09:15–12:30 | Deep work block 1 | Small PRs |
| 12:30–13:00 | Integration: `git pull` + `./scripts/dev.sh` | Nothing broken across tracks |
| 13:00–17:30 | Deep work block 2 | |
| 17:30–18:00 | Demo of the day (5 min / track) | `docs/progress/day-XX.md` (+ mp4 when recorded) |
| 18:00–18:30 | Acceptance + merge + `git tag day-XX` | Tagged release |

## Git rules
- Branches: `fe/*` · `be/*` · `ai/*` · `lab/*`
- PR ≤ 400 lines
- Conventional commits: `feat(fe): …`
- **No direct push to `main` after day 3** — open a PR
