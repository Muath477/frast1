# Demo backup video (v1)

**Target:** OBS 1920×1080, ≤ 5:00, same script as `DEMO_SCRIPT.md`, clear voice → `docs/demo-backup.mp4`

## Record checklist

1. Presenter Mode on · preflight ✔ · `demo-reset.sh`
2. OBS: Canvas 1920×1080, display + mic, no desktop audio spam
3. Run the 5-minute script once without stopping
4. Export MP4 H.264 · confirm duration ≤ 5:00
5. Copy to **three places**:
   - `docs/demo-backup.mp4` (this repo — git-lfs or external if large)
   - USB stick (presentation bag)
   - Google Drive team folder

## Status (Day 12)

| Place | Status |
|---|---|
| `docs/demo-backup.mp4` | Pending OBS on demo laptop (script + measured numbers ready) |
| USB | Pending after record |
| Google Drive | Pending after record |

Day 13 records **v2** after dress rehearsals. Until the file exists, failover is `POST /api/demo/mode {"mode":"sim"}` with the on-screen SIMULATION badge.
