# RootIQ

**Find the cause before it becomes an outage** — alert storm → one incident → evidence-backed RCA → engineer approve-only remediation in under 60 seconds.

![RootIQ demo](docs/deck/rootiq-demo.gif)

Venture X Hackathon — Infrastructure & Cloud · Mode: **sim-first** (live EVE-NG additive)

## كيف تشغّل المشروع / How to run

### أول مرة فقط (once)

```powershell
cd e:\frast1\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

cd e:\frast1\frontend
npm install
```

### كل مرة (every time) — طرفيتان

**1) Backend (sim)**
```powershell
cd e:\frast1\backend
.\.venv\Scripts\Activate.ps1
$env:ROOTIQ_MODE = 'sim'
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**2) Frontend** (طرفية ثانية)
```powershell
cd e:\frast1\frontend
npm run dev
```

**3) افتح المتصفح**
- UI: http://localhost:5173
- API health: http://localhost:8000/api/health

### ديمو سريع
`Shift+P` Presenter · `Shift+1` ازدحام · Reject / Approve · `Shift+R` إعادة

### Docker (اختياري)
```powershell
cd e:\frast1
docker compose up -d --build
# UI http://localhost:8080  ·  API http://localhost:8000
./scripts/preflight.sh
```

### نشر عام (رابط للمشاركة)
**الآن (نفق Cloudflare — اللابتوب لازم يظل شغّال):** الرابط يظهر من `cloudflared tunnel --url http://127.0.0.1:5173`

**دائم (Render — باك+فرونت في صورة واحدة):** ادفع الريبو ثم افتح  
https://dashboard.render.com/select-repo?type=blueprint  
واختر `iksasa15/frast1` (يستخدم `render.yaml` + `Dockerfile`).

## Architecture

Lab collector → FastAPI ingest → detect/correlate/RCA/explain → WebSocket UI → approve → whitelisted lab agent.

Full Mermaid + 30s verbal: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Multi-agent layer

14 specialised agents (telemetry → detection → correlation/topology → RCA → explanation/knowledge → remediation → guardrail → **human** → execution → verification → learning) plus a read-only bilingual **Copilot** with a local **RAG** index. Twelve agents are fully deterministic; the LLM (Claude / Gemini / Groq) is optional and can only reword text with numbers grounded in measurements.

- Per-agent benefit, needs, guardrails and failure behaviour: [`docs/AGENTS.md`](docs/AGENTS.md)
- Big picture, spec compliance matrix, gaps, roadmap: [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md)
- UI: **Agents** page (roster, live trace, Copilot) · API: `GET /api/agents`, `POST /api/copilot/ask`

## Modes

| | |
|---|---|
| `ROOTIQ_MODE=sim` | In-process simulator (default, offline, backup) |
| `ROOTIQ_MODE=live` | EVE-NG + COLLECTOR-01 + lab agent |

UI badge always shows the active mode.

## Measured results

From `GET /api/runs` (9 sim runs) — details in [`docs/RESULTS.md`](docs/RESULTS.md):

| Metric | Target | Measured |
|---|---|---|
| Time to RCA | &lt; 60 s | **12.3 s** |
| Top-1 root | Top 3 | **9/9** |
| Noise reduction | 30% | **96.3%** |
| Human approval | 100% | **100%** |

## Pitch & demo

- Deck: [`docs/RootIQ_Pitch_Deck_Final.pptx`](docs/RootIQ_Pitch_Deck_Final.pptx) (numbers from RESULTS)
- **Demo day runbook:** [`docs/RUNBOOK.md`](docs/RUNBOOK.md)
- Script: [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) · Q&A: [`docs/QA_BANK.md`](docs/QA_BANK.md)
- Risks · compressed plans · solo path: [`docs/RISKS.md`](docs/RISKS.md) · [`COMPRESSED_PLANS.md`](docs/COMPRESSED_PLANS.md) · [`SOLO_PATH.md`](docs/SOLO_PATH.md)
- Rehearsal / bag: [`docs/REHEARSAL.md`](docs/REHEARSAL.md) · [`docs/BAG.md`](docs/BAG.md)
- Backup video: [`docs/demo-backup.md`](docs/demo-backup.md)
- Full docs index: [`docs/README.md`](docs/README.md)
- Ship tag: **`v1.0`**

## Demo hotkeys

Shift+1 uplink · Shift+2 DNS · Shift+3 server spike · Shift+R reset · Shift+P presenter

## Team

| Role | Who |
|---|---|
| FE / keyboard demo | Ahmed |
| BE / AI / INFRA / Presenter | Team (see kickoff) |

## Docs

Index: [`docs/README.md`](docs/README.md) · Full plan: `RootIQ_Daily_Plan.md` · Progress: `docs/progress/`

## Feature freeze

After Day 11 / `v1.0-rc1`: **no new features** — bugfixes only with two-person review.
