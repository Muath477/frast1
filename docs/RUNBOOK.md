# Day 14 — Demo day runbook

**Ship tag:** `v1.0` · **Script:** `docs/DEMO_SCRIPT.md` · **Q&A:** `docs/QA_BANK.md` · **Failover:** `docs/REHEARSAL.md` · **Bag:** `docs/BAG.md`

Numbers spoken aloud come from `docs/RESULTS.md` (already filled into the script).

---

## T-minus schedule

| Time | Action | Owner | ☐ |
|---|---|---|---|
| **T−120** | Arrive · HDMI · confirm **1920×1080** · OS zoom **100%** | Presenter | ☐ |
| **T−90** | EVE boot order: **R1 → SW1/SW2 (wait ~90s) → APP-01 → COLLECTOR-01** · `systemctl status rootiq-collector rootiq-lab-agent` | INFRA | ☐ |
| **T−60** | `docker compose up -d` → `./scripts/preflight.sh` all ✔ (video optional) | BE | ☐ |
| **T−45** | One full dry run (live if lab up, else sim) → `./scripts/demo-reset.sh` | **FE (Ahmed)** | ☐ |
| **T−30** | Do Not Disturb · close everything except **Dashboard (Presenter Mode)** + **Deck** | Presenter | ☐ |
| **T−15** | **Baseline warm 10 minutes — do not inject** | ALL | ☐ |
| **T−5** | Final `./scripts/preflight.sh` · backup video open in a **hidden** tab | FE | ☐ |
| **T** | Pitch + demo per `DEMO_SCRIPT.md` | Presenter + FE keyboard | ☐ |
| **T+** | **Leave everything running** — judges often ask for a second try | ALL | ☐ |

---

## FE cue card (Ahmed — keyboard only)

| Cue | Key / click |
|---|---|
| Presenter Mode | `Shift+P` |
| Link R1↔SW1 | Click `r1–sw1` |
| Inject uplink | `Shift+1` |
| Reject flow | Reject → `Outside change window` → Confirm reject |
| Approve | Approve Remediation |
| Analytics beat | Navigate Analytics |
| Reset mid-ask | `Shift+R` |
| Other scenario | `Shift+R` then `Shift+2` |
| EVE dead | Settings → **Use Simulation feed** (badge = SIMULATION) |

---

## Measured lines (do not invent)

| Beat | Say |
|---|---|
| Alert storm | **~33** alerts |
| Stopwatch / RCA | **~11 s** (target &lt; 60) |
| Lab series | **9** runs · Top-1 **9/9** · noise ↓ **~96%** |
| Evidence (sim design) | util **~97%** · latency **~2 → ~86 ms** · service lag **~6 s** after link |
| Recover (uplink avg) | detect **&lt;1 s** · RCA **~11 s** · recover **~27 s** |

Source: `docs/RESULTS.md` + uplink scenario targets in simulator.

---

## Golden rules

1. Do **not** read the screen.
2. Never say «إن شاء الله يشتغل».
3. Unexpected: «This is live — let me show you» → Day-13 failover.
4. Judges should see **numbers** more than talk.
5. After the pitch: **do not power anything down**.

---

## If something breaks at T

| Symptom | Immediate |
|---|---|
| EVE frozen | «recorded lab feed» → Simulation |
| Backend dead | `docker compose restart backend` |
| Laptop dead | Spare laptop **or** `docs/demo-backup.mp4` |
| Wrong scenario request | `Shift+R` → `Shift+2` |
| RCA looks off | CandidateRanking talking point → re-inject |
