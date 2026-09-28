# Day 13 — Final rehearsal · emergency drills · v1.0

## Acceptance
- [x] Rehearsal schedule + log template — `docs/REHEARSAL.md`
- [x] Emergency drills scripted — `backend/scripts/emergency_drills.py` (&lt;30s paths)
- [x] Settings **Use Simulation feed** failover button (badge stays honest: SIMULATION)
- [x] Bag / build checklist — `docs/BAG.md`
- [ ] 3 live stopwatch rehearsals with outsider judge — team on venue day (log in REHEARSAL)
- [ ] OBS video v2 ≤5:00 in repo + USB + Drive — `docs/demo-backup.md`
- [x] Tag **`v1.0`** (ship tag for the pitch)

## Drill command
```powershell
cd backend
.\.venv\Scripts\python.exe scripts\emergency_drills.py
```

## Notes
Feature freeze still holds — only failover UX that Day 13 required (Settings mode) and docs/scripts.
