# RootIQ

**Find the cause before it becomes an outage** — alert storm → one incident → evidence-backed RCA → engineer approve-only remediation in under 60 seconds.

![RootIQ demo](docs/deck/rootiq-demo.gif)

Venture X Hackathon — Infrastructure & Cloud · Mode: **sim-first** (live EVE-NG additive)

> **الفرع `my-edits`** يحوي كل تعديلات الطبقة الذكية (الوكلاء، قاعدة المصنّعين، التدريب). إن رأيتَ README قديمًا فأنت على `main`: بدّل الفرع من قائمة الفروع في أعلى صفحة GitHub إلى **`my-edits`**، أو اقرأ [`CHANGELOG.md`](CHANGELOG.md).
> *This branch (`my-edits`) holds all the AI-layer work: agents, the vendor knowledge base and the training folder. On GitHub, switch the branch selector to `my-edits`.*

## ما الجديد في هذا الفرع · What's new

| المجال | ماذا أُضيف | التفاصيل |
|---|---|---|
| **16 وكيلًا** | من 14 إلى 16: `vendor` (هوية الجهاز + أوامر كل مصنّع) و`logs` (Syslog متعدد المصنّعين). Guardrail يفرض أن أوامر التشخيص للقراءة فقط | [`docs/AGENTS.md`](docs/AGENTS.md) |
| **قاعدة معرفة المصنّعين** | 43 مصنّعًا · 59 نظام تشغيل · 103 عائلة أجهزة · 25 نمط مشكلة · 26 «قدرة» موحّدة، بتغطية وثقة معلنتين لكل مصنّع | [`docs/VENDORS.md`](docs/VENDORS.md) |
| **Cisco + Juniper + Fortinet + Aruba + Arista** | لكل نظام: أوامر الفحص بصيغته، **طريقة حفظ الإعداد** (`write memory` / `commit` / حفظ تلقائي)، التراجع، وأسلوب كتابة الأوامر | [`docs/VENDORS.md` §3b](docs/VENDORS.md) |
| **Syslog** | `POST /api/syslog`: سطر «المنفذ سقط» من أي مصنّع مدعوم يفتح حادثة على الرابط الصحيح | [`docs/AGENTS.md` §4.15](docs/AGENTS.md) |
| **Copilot + RAG** | يجيب عن أوامر ومشاكل وحفظ الإعداد لأي مصنّع (حتى 4 جنبًا إلى جنب)، حرفيًا من القاعدة وبمصدر | [`docs/AGENTS.md` §4.9](docs/AGENTS.md) |
| **الواجهة** | في خطة الحادثة: «Vendor diagnostics» و«Applying a change»؛ وصفحة Agents فيها 16 وكيلًا | `frontend/src/components/incidents/VendorCommands.tsx` |
| **التدريب** | مجلد [`training/`](training/README.md): بيانات مولَّدة من القاعدة (≈4.7 ألف مثال EN/AR في 10 مهام)، مقيّم آلي، كتالوج Hugging Face، ودفتر Colab | [`training/README.md`](training/README.md) · [`docs/AI_TRAINING.md`](docs/AI_TRAINING.md) |
| **معمل متعدد المصنّعين** | مثال جاهز: Cisco + Juniper vQFX + Arista vEOS + FortiGate-VM + Aruba AOS-CX | [`configs/topology.multivendor.example.json`](configs/topology.multivendor.example.json) |
| **الاختبارات** | 262 backend (كانت 151) + اختبارات بيانات التدريب والدفتر | `cd backend && pytest -q` |

سجل التغييرات الكامل: [`CHANGELOG.md`](CHANGELOG.md).

### جرّبها في دقيقتين (بعد تشغيل الـbackend)

```bash
# 1) هوية جهاز من sysDescr
curl -s -X POST localhost:8000/api/vendors/identify -H 'content-type: application/json' \
  -d '{"sysDescr":"Juniper Networks, Inc. ex4300-48t Ethernet Switch, kernel JUNOS 21.4R3-S5.4, Build date: 2023-06-01 10:00:00 UTC Copyright (c) 1996-2023 Juniper Networks, Inc."}'

# 2) سطر syslog يفتح حادثة (نفس رمز /api/events)
curl -s -X POST localhost:8000/api/syslog -H 'content-type: application/json' -H 'x-rootiq-token: change-me-ingest' \
  -d '{"device":"r1","lines":["%LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to down"]}'

# 3) الـCopilot: كيف يُحفظ الإعداد على أكثر من مصنّع؟
curl -s -X POST localhost:8000/api/copilot/ask -H 'content-type: application/json' \
  -d '{"question":"How do I save the config on Junos vs Cisco vs Fortigate?"}'
```

### ما لا يدّعيه المشروع (بصراحة)
- القاعدة **ليست شاملة**: 5 مصنّعين بتغطية كاملة و7 جزئية و31 «تعريف فقط»؛ الموديلات بمستوى **العائلة/السلسلة** لا كل SKU.
- الأوامر وأنماط syslog كُتبت من المعرفة العامة ولم تُلتقط من أجهزة حقيقية (لكل مصنّع علامة ثقة؛ **Fortinet الأضعف**). RootIQ يعرضها للمهندس ولا يدفعها لأي جهاز.
- التدريب على GPU (Colab) لم يُشغَّل هنا؛ أما توليد البيانات والمقيّم وخلايا الدفتر التي بلا GPU فمُختبرة.

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

16 specialised agents (telemetry/logs → detection → correlation/topology → RCA → explanation/knowledge/**vendor** → remediation → guardrail → **human** → execution → verification → learning) plus a read-only bilingual **Copilot** with a local **RAG** index. Fourteen agents are fully deterministic; the LLM (Claude / Gemini / Groq) is optional and can only reword text with numbers grounded in measurements.

- Per-agent benefit, needs, guardrails and failure behaviour: [`docs/AGENTS.md`](docs/AGENTS.md)
- Big picture, spec compliance matrix, gaps, roadmap: [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md)
- **Vendor-aware:** a knowledge base of 43 network vendors (identity from `sysDescr`/`sysObjectID`, per-vendor read-only diagnostics, syslog formats, 25 problem patterns) feeds the `vendor` and `logs` agents: [`docs/VENDORS.md`](docs/VENDORS.md). Training data generated from it: [`training/`](training/README.md).
- UI: **Agents** page (roster, live trace, Copilot) · API: `GET /api/agents`, `POST /api/copilot/ask`
- One command (Windows): `powershell -ExecutionPolicy Bypass -File .\scripts\run-demo.ps1` starts the backend + UI in simulation mode and opens the Agents page. Optional LLM: `$env:GROQ_API_KEY='...'` then add `-Llm groq` (the key is read from the environment and never stored). Stop with `-Stop`.

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

## Tests & training data

```powershell
cd backend
$env:ROOTIQ_MODE = 'sim'
.\.venv\Scripts\python.exe -m pytest -q                        # 262 tests
cd ..\frontend; npx tsc --noEmit; npx vitest run src           # type-check + unit tests
cd ..; python training\build_dataset.py --check                # committed training data matches the knowledge base
```

## Docs

Index: [`docs/README.md`](docs/README.md) · Full plan: `RootIQ_Daily_Plan.md` · Progress: `docs/progress/` · What changed: [`CHANGELOG.md`](CHANGELOG.md)

| Read this | For |
|---|---|
| [`docs/AGENTS.md`](docs/AGENTS.md) | The 16 agents: benefit, needs, guardrails, failure behaviour, API, tests; what was added / modified for multi-vendor support (§4b) |
| [`docs/VENDORS.md`](docs/VENDORS.md) | Vendor knowledge base: coverage table, config model per vendor (§3b), how to add a vendor, honest limits |
| [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md) | Big picture, spec compliance, gaps, roadmap |
| [`docs/AI_TRAINING.md`](docs/AI_TRAINING.md) · [`training/README.md`](training/README.md) | What to train and why, the generated dataset, the evaluator, Hugging Face catalog, the Colab notebook |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Diagram + 30-second explanation |

## Feature freeze

After Day 11 / `v1.0-rc1`: **no new features** — bugfixes only with two-person review.
