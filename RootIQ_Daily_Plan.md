# RootIQ — الخطة التنفيذية اليومية الكاملة (React + FastAPI + EVE-NG)

> **الهدف:** المركز الأول في Venture X Hackathon — مسار Infrastructure & Cloud
> **الوعد اللي لازم نثبته قدام الحكام بعرض حي:** «من عشرات التنبيهات المتفرقة إلى حادثة واحدة، بسبب جذري مدعوم بأدلة، وإجراء لا يُنفّذ إلا بموافقة المهندس — خلال أقل من 60 ثانية».
> **مصادر الخطة:** `RootIQ_Platform_Implementation_Specification.docx` + `RootIQ_Pitch_Deck_Final.pptx` + `داعم.rtf`

---

## 0. كيف تستخدم هذا الملف

- الخطة مبنية على **14 يوم عمل + يوم صفر (اليوم)**. لو المدة عندكم أقصر، شوف القسم **«ضغط الخطة»** في آخر الملف (نسخة 7 أيام ونسخة 48 ساعة).
- كل يوم فيه: **الهدف ← المخرجات ← مهام كل مسار (بالأوامر والمسارات والكود) ← معايير القبول القابلة للتحقق ← إغلاق اليوم**.
- رموز المسارات:
  - 🟦 **FE** — Frontend (React) — **أنت (أحمد)**
  - 🟩 **BE** — Backend (FastAPI + PostgreSQL + WebSocket)
  - 🟨 **AI** — الذكاء والتحليل (Baseline + Anomaly + Graph + RCA + Explanation)
  - 🟥 **INFRA** — المختبر (EVE-NG + الأجهزة + الخدمات + سكربتات الأعطال)
  - ⬜ **ALL** — الفريق كامل
- **قاعدة ذهبية:** لا ينتهي أي يوم إلا وكل معايير القبول ✅ ومدموجة في `main` ومعلّم عليها `git tag day-XX`. اللي ما اكتمل ينتقل لأول ساعتين من اليوم التالي، وما نبدأ جديد قبله.
- **لو كنت تشتغل لحالك أو الفريق صغير:** نفّذ 🟦 و🟩 و🟨 كاملة معتمدًا على **Simulator Mode**، وخلّ 🟥 المختبر الحي إضافة لاحقة. شوف قسم «لو الفريق صغير» في النهاية.

---

## 1. استراتيجية الفوز (ليش هالخطة تجيب المركز الأول)

| معيار التحكيم المعتاد | وش نقدّم عشان نتفوق | متى نبنيه |
|---|---|---|
| الابتكار | RCA هجين قابل للتفسير (قواعد + Graph + Anomaly + شرح مقيّد بالأرقام) بدل «AI صندوق أسود» | اليوم 7–9 |
| العمق التقني | مختبر EVE-NG **حقيقي** + SNMP + Syslog + QoS يُطبّق فعليًا على الراوتر بعد الموافقة | اليوم 2–8 |
| جودة المنتج/الواجهة | خريطة React Flow حيّة بالمنافذ، روابط متحركة حسب الحمل، لوحة حادثة احترافية | اليوم 1–10 |
| الأثر والقيمة | أرقام **مقاسة فعليًا** على الشاشة: MTTD، MTTR، نسبة تقليل الضجيج (Noise Reduction) | اليوم 9–12 |
| الجاهزية والموثوقية | الديمو يشتغل 3 مرات متتالية + وضع محاكاة احتياطي + فيديو احتياطي | اليوم 11–13 |
| العرض | قصة 5 دقائق محكمة، مع لحظة «واو»: عاصفة 20+ تنبيه تنطوي في حادثة واحدة | اليوم 12–13 |

### أسلحة التميّز (Differentiators) اللي ما راح تلقاها عند الفرق الثانية
1. **Alert Storm → One Incident:** عمود يسار يعرض التنبيهات الخام تتدفق (مثل أي أداة تقليدية)، ويمينه RootIQ يجمعها في حادثة وحدة + عداد «Noise Reduction 95%».
2. **MTTD Stopwatch:** ساعة كبيرة تبدأ لحظة ضغط Inject وتوقف لحظة ظهور السبب الجذري. الحكام يشوفون الرقم بعيونهم.
3. **Why this cause? (Explainability):** أعلى 3 مرشحين مع تفكيك الدرجة (5 مكونات) كأشرطة ملونة + سبب استبعاد المرشحين الآخرين («DNS عرَض وليس سبب لأنه خلف الرابط المزدحم»).
4. **Grounded Explanation Guard:** الشرح بالعربي والإنجليزي؛ ولو استُخدم LLM فأي رقم في الشرح ما هو موجود في الأدلة المقاسة → نرفض الشرح ونرجع للقالب. (نقطة قوية جدًا قدام الحكام ضد الهلوسة).
5. **إجراء حقيقي بعد الموافقة:** عند Approve يُطبَّق `service-policy UPLINK-QOS` فعليًا على R1 عبر Netmiko وتنخفض الـLatency قدامهم.
6. **Learning from resolved incidents:** كل حادثة تنحل تزيد `historical_support` للسبب نفسه في المرات القادمة («شوهد 3 مرات سابقًا»).
7. **Arabic-first toggle:** واجهة وشرح بالعربي RTL بضغطة — ميزة محلية للسوق السعودي.
8. **Live ⇄ Simulation hot switch:** لو المختبر خرب وسط العرض، تتحول لوضع المحاكاة بدون ما تعيد تحميل الصفحة، مع شارة واضحة (شفافية).

### ترتيب البناء الإلزامي (من الوثيقة نفسها)
**الخريطة أولًا ← مؤشر واحد يتحرك حيًّا ← لوحة الحادثة ← RCA ← الموافقة ← باقي السيناريوهات ← الـLLM أخيرًا.** لا تبدأ بالنموذج اللغوي أبدًا.

---

## 2. القرارات المجمّدة (تتقرر في اليوم صفر وما تتغير)

### 2.1 الطوبولوجيا النهائية (نجمة حول R1)
اخترنا تصميم ملف `داعم.rtf` (R1 متصل بـSW1 وSW2) بدل تصميم الـdocx (SW1↔SW2)، **لأن سيناريو الازدحام لازم يمر فيه مسار الخدمة عبر R1 Gi0/0**. بتصميم الـdocx حركة Collector→APP ما تمر على R1 أصلًا، فيسقط الديمو.

```text
                 ┌──────────────┐
                 │ R1 (vIOS)    │  Lo0 10.10.10.1 (management)
                 └─┬─────────┬──┘
     Gi0/0 10.10.20.1│         │Gi0/1 10.10.30.1
     (shaped 10 Mbps)│         │
          Gi0/1 ┌────┴──┐   ┌──┴────┐ Gi0/1
                │ SW1   │   │ SW2   │
                │.20.11 │   │.30.12 │
          Gi0/3 └───┬───┘   └───┬───┘ Gi0/3
                    │           │
             eth0 ┌─┴──────┐ ┌──┴──────────┐ ens3
                  │ APP-01 │ │ COLLECTOR-01│  + ens4 → EVE Cloud (mgmt → لابتوب العرض)
                  │.20.10  │ │ .30.10      │
                  │DNS+Web │ │collector +  │
                  └────────┘ │lab-agent    │
                             └─────────────┘
مسار الخدمة: COLLECTOR-01 → SW2 → R1(Gi0/1→Gi0/0) → SW1 → APP-01
```

| الجهاز | الصورة في EVE-NG | العنوان | المنافذ |
|---|---|---|---|
| R1 | Cisco vIOS (IOSv) | Lo0 `10.10.10.1/32` · Gi0/0 `10.10.20.1/24` · Gi0/1 `10.10.30.1/24` | Gi0/0→SW1 Gi0/1 · Gi0/1→SW2 Gi0/1 |
| SW1 | Cisco vIOS-L2 | Vlan1 `10.10.20.11/24` | Gi0/1→R1 · Gi0/3→APP-01 |
| SW2 | Cisco vIOS-L2 | Vlan1 `10.10.30.12/24` | Gi0/1→R1 · Gi0/3→COLLECTOR-01 |
| APP-01 | Ubuntu Server 24.04 | `10.10.20.10/24` gw `.1` | eth0→SW1 Gi0/3 |
| COLLECTOR-01 | Ubuntu Server 24.04 | ens3 `10.10.30.10/24` gw `.1` · ens4 DHCP (Cloud) | ens3→SW2 Gi0/3 |

> ملاحظة: لو استخدمتوا صور IOL بدل vIOS، أسماء المنافذ تصير `Ethernet0/0`… غيّرها **فقط** في `configs/topology.json` — ممنوع أي اسم منفذ مكتوب داخل الكود.

### 2.2 أين يشتغل كل شيء
| المكوّن | المكان | المنفذ |
|---|---|---|
| PostgreSQL 16 | لابتوب العرض (Docker) | 5432 |
| Backend FastAPI | لابتوب العرض (Docker) | 8000 |
| Frontend (dev) | لابتوب العرض | 5173 (بروكسي لـ8000) |
| Frontend (build) | لابتوب العرض (nginx داخل Docker) | 8080 |
| Collector | COLLECTOR-01 داخل المختبر | يدفع إلى `http://<LAPTOP_IP>:8000/api/events/batch` |
| Lab-Agent (حقن وعلاج بأوامر مسموحة فقط) | COLLECTOR-01 | 9000 |
| App-01 host agent (psutil) | APP-01 | 9100 |

### 2.3 الـStack (مجمّد)
- **Frontend:** Vite + React 19 + TypeScript + Tailwind CSS v4 + `@xyflow/react` (React Flow v12) + Zustand + React Router + Recharts + `motion` + `lucide-react` + `i18next` + Vitest + Playwright.
- **Backend:** Python 3.12 + FastAPI + Pydantic v2 + SQLAlchemy 2 + psycopg 3 + NetworkX + NumPy + scikit-learn + httpx + pytest.
- **Lab:** EVE-NG Community + vIOS/vIOS-L2 + Ubuntu 24.04 + bind9 + nginx + iperf3 + stress-ng + net-snmp + Netmiko.
- **وضعا التشغيل:** `ROOTIQ_MODE=live` (مختبر حقيقي) و`ROOTIQ_MODE=sim` (محاكاة بنفس صيغة الأحداث تمامًا). **الواجهة ما تعرف الفرق** إلا من الشارة.

### 2.4 عقد الأحداث الموحّد (Normalized Event) — مرجع وحيد
```json
{
  "eventId": "evt-00042",
  "timestamp": "2026-10-05T18:30:00Z",
  "sourceId": "link-r1-sw1",
  "sourceType": "link",
  "metric": "link_utilization",
  "value": 97.2,
  "unit": "percent",
  "interface": "Gi0/0",
  "severity": "info",
  "metadata": {"device": "r1", "peer": "sw1", "collector": "snmp"}
}
```
`sourceType ∈ router | switch | server | collector | link | service`

| metric | الوحدة | يُرسل على | warning | critical |
|---|---|---|---|---|
| `link_utilization` | percent | link | ≥ 70 | ≥ 85 |
| `link_latency_ms` (فرق زمن الـhop) | ms | link | ≥ 3× baseline أو ≥ 30 | ≥ 60 |
| `link_packet_loss` | percent | link | ≥ 1 | ≥ 5 |
| `if_out_discards_rate` | pps | link | > 5 | > 50 |
| `if_oper_status` | 1/0 | link | — | = 0 |
| `cpu_percent` / `mem_percent` | percent | server | ≥ 80 / 85 | ≥ 95 |
| `http_latency_ms` | ms | service `svc-web` | ≥ 300 | ≥ 1000 |
| `http_ok` | 1/0 | service `svc-web` | — | = 0 |
| `dns_success_rate` | percent | service `svc-dns` | < 95 | < 50 |
| `dns_latency_ms` | ms | service `svc-dns` | ≥ 100 | ≥ 500 |

### 2.5 رسائل WebSocket (`/ws/operations`) — ظرف موحّد `{type, ts, data}`
| type | data | التردد |
|---|---|---|
| `snapshot` | الطوبولوجيا + حالة كل رابط/جهاز/خدمة + الحوادث المفتوحة + الوضع | مرة عند الاتصال |
| `link` | `{id,status,utilization,latencyMs,packetLoss}` | ≤ 1/ثانية لكل رابط |
| `node` | `{id,status,metrics}` | ≤ 1/ثانية |
| `service` | `{id,status,metrics}` | ≤ 1/ثانية |
| `alert` | تنبيه خام `{id,sourceId,metric,value,severity,ts}` | عند كل عبور عتبة |
| `incident` | كائن الحادثة كامل | عند أي تغيير |
| `demo` | `{mode,scenario,state,injectedAt}` | عند الحقن/العلاج/إعادة الضبط |

### 2.6 دورة حياة الحادثة
`open → investigating → recommendation_ready → awaiting_approval → approved | rejected → resolved`
(الرفض ما يغيّر المختبر ويُسجّل السبب؛ بعد الرفض تبقى الحادثة `awaiting_approval` لقرار جديد.)

---

## 3. هيكل المستودع النهائي

```text
rootiq/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/config.py
│   │   ├── db/session.py
│   │   ├── db/models.py
│   │   ├── schemas/{common,event,topology,incident,action}.py
│   │   ├── api/{health,topology,events,incidents,actions,demo,runs,ws}.py
│   │   ├── services/{hub,state_store,topology_service,pipeline,incident_service,action_service,recorder,lab_client}.py
│   │   ├── intelligence/{baseline,anomaly,graph,correlate,rca,history,explain}.py
│   │   └── collectors/simulator.py
│   ├── tests/{test_graph,test_baseline,test_correlate,test_rca,test_explain,test_api}.py
│   ├── tests/fixtures/*.jsonl
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.tsx · App.tsx · index.css
│   │   ├── lib/{types,api,ws,colors,format,layout}.ts
│   │   ├── store/useOps.ts
│   │   ├── hooks/{useOpsSocket,useHotkeys}.ts
│   │   ├── i18n/{index.ts,en.json,ar.json}
│   │   ├── components/layout/{Shell,Sidebar,TopBar,KpiStrip,ModeBadge}.tsx
│   │   ├── components/topology/{TopologyCanvas,DeviceNode,PortEdge,LinkInspector,DeviceInspector}.tsx
│   │   ├── components/incidents/{IncidentPanel,ConfidenceRing,CandidateRanking,EvidenceList,AffectedServices,ActionCard,RejectDialog}.tsx
│   │   ├── components/timeline/Timeline.tsx
│   │   ├── components/demo/{DemoControls,AlertStorm,MttdStopwatch}.tsx
│   │   └── pages/{OperationsPage,IncidentsPage,DevicesPage,AnalyticsPage,AuditPage,SettingsPage}.tsx
│   ├── e2e/demo.spec.ts
│   ├── vite.config.ts · playwright.config.ts · Dockerfile · nginx.conf
├── lab/
│   ├── eve/rootiq.unl                # تصدير المختبر
│   ├── configs/{r1,sw1,sw2}.cfg
│   ├── app01/{setup.sh,agent.py,rootiq-agent.service,db.rootiq.lab,named.conf.local}
│   ├── collector/{collector.py,requirements.txt,rootiq-collector.service}
│   ├── agent/{lab_agent.py,rootiq-lab-agent.service}
│   └── scenarios/{uplink_congestion.sh,dns_failure.sh,server_spike.sh,reset.sh}
├── configs/
│   ├── topology.json
│   └── layout.json
├── scripts/{dev.sh,preflight.sh,demo-reset.sh,rehearse.sh}
├── docs/{CONTRACTS.md,ARCHITECTURE.md,DEMO_SCRIPT.md,QA_BANK.md,RESULTS.md}
├── data/recordings/                 # تسجيلات الأحداث (gitignored)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 4. الإيقاع اليومي (ثابت لكل يوم)

| الوقت | النشاط | المخرج |
|---|---|---|
| 09:00–09:15 | Standup: أمس / اليوم / العوائق | تحديث لوحة المهام |
| 09:15–12:30 | Deep work بلوك 1 | PRs صغيرة |
| 12:30–13:00 | **Integration check**: `git pull && ./scripts/dev.sh` وكل واحد يتأكد إن شغل الثاني ما كسر شغله | |
| 13:00–17:30 | Deep work بلوك 2 | |
| 17:30–18:00 | **Demo of the day** (5 دقائق لكل مسار على الشاشة) | تسجيل شاشة قصير في `docs/progress/day-XX.mp4` |
| 18:00–18:30 | التحقق من معايير القبول + merge + `git tag day-XX && git push --tags` | |

**قواعد Git:** فروع `fe/*` `be/*` `ai/*` `lab/*` · PR ≤ 400 سطر · Conventional commits (`feat(fe): ...`) · ممنوع push مباشر على `main` بعد اليوم 3.

---

## 5. نظرة عامة على الأيام

| اليوم | العنوان | 🟦 أنت (FE) | معلَم التحقق |
|---|---|---|---|
| 0 | الانطلاق وتجميد القرارات | إنشاء الريبو والأدوات | القرارات موقّعة في `docs/CONTRACTS.md` |
| 1 | الأساس | Vite + Tailwind + React Flow يرسم `topology.json` ثابت | 5 أجهزة تظهر |
| 2 | الطوبولوجيا الحقيقية | Custom Nodes بمنافذ + Custom Edges بأسماء المنافذ + حفظ Layout | الروابط مربوطة بالمنافذ الصحيحة |
| 3 | خط البيانات الحي | WebSocket + Zustand + تحديث الروابط بدون Refresh | رقم يتحرك على الخريطة |
| 4 | Collector حي | Shell كامل + KPI + Inspectors + Sparklines | بيانات المختبر الحقيقية على الشاشة |
| 5 | حقن الأعطال | DemoControls + Hotkeys + تدفق التنبيهات الخام | **M1:** Inject يغيّر الخريطة (sim + live) |
| 6 | الحوادث | IncidentPanel v1 + قائمة الحوادث + Timeline v1 | عطل واحد = حادثة واحدة |
| 7 | RCA | CandidateRanking + ConfidenceRing + تلوين السبب/المسار | **M2:** سبب صحيح < 60 ث |
| 8 | الإجراء والتعافي | ActionCard + RejectDialog + Audit + Resolved | **M3:** الحلقة كاملة للسيناريو 1 |
| 9 | السيناريو 2 و3 + لحظة الواو | AlertStorm + MTTD Stopwatch + Noise Reduction | 3 سيناريوهات تنجح |
| 10 | التميّز | عربي RTL + Replay + Analytics + Presenter Mode | لقطات جاهزة للعرض |
| 11 | التصليب والاختبارات | Playwright ×3 + Build إنتاجي + Hot switch | **Feature Freeze** |
| 12 | العرض والقصة | لقطات + فيديو احتياطي v1 | Deck بأرقام حقيقية |
| 13 | البروفة النهائية | 3 بروفات كاملة + تدريبات أعطال | فيديو نهائي |
| 14 | يوم العرض | Runbook | 🏆 |

---

# اليوم 0 — الانطلاق وتجميد القرارات (ساعتين إلى 3 ساعات، اليوم نفسه)

**الهدف:** كل الفريق يطلع من الاجتماع وهو عارف: الطوبولوجيا، العقود، الأدوار، الريبو، وموعد كل معلَم.

### ⬜ ALL — اجتماع الانطلاق (90 دقيقة)
1. (15د) قراءة القسم 1 و2 من هذا الملف بصوت عالي.
2. (20د) توقيع الطوبولوجيا (2.1) — أي اعتراض الحين أو أبدًا.
3. (20د) توقيع عقد الأحداث (2.4) ورسائل WS (2.5) — هذا «API» بين المسارات الأربعة.
4. (15د) توزيع الأدوار (القسم 17 في الـdocx): FE = أحمد · BE = ؟ · AI = ؟ · INFRA = ؟ · **مسؤول العرض (Presenter)** = ؟ · **مسؤول الوقت** = ؟
5. (10د) تحديد تاريخ يوم العرض الفعلي وربطه بجدول الأيام، وقرار: هل نحتاج «ضغط الخطة»؟
6. (10د) التأكد من موارد جهاز EVE-NG: **16GB RAM على الأقل** (المختبر يحتاج ≈ 7GB).

### 🟦 FE (أنت) — إنشاء المستودع
```bash
# 1) تحقق من الأدوات
node -v            # المطلوب ≥ 20.19 (أو 22.x)
npm -v
python3.12 --version
docker compose version
git --version

# 2) إنشاء المستودع
mkdir -p ~/dev/rootiq && cd ~/dev/rootiq && git init -b main
mkdir -p backend/app/{core,db,schemas,api,services,intelligence,collectors} backend/tests/fixtures \
         lab/{eve,configs,app01,collector,agent,scenarios} configs scripts docs/progress data/recordings
touch backend/app/__init__.py backend/app/{core,db,schemas,api,services,intelligence,collectors}/__init__.py backend/tests/__init__.py

cat > .gitignore << 'GI'
data/recordings/
.env
__pycache__/
.venv/
node_modules/
dist/
.pytest_cache/
playwright-report/
test-results/
*.pyc
GI

cat > .env.example << 'ENV'
ROOTIQ_MODE=sim                      # sim | live
DATABASE_URL=postgresql+psycopg://rootiq:rootiq@db:5432/rootiq
TOPOLOGY_PATH=/app/configs/topology.json
LAYOUT_PATH=/app/configs/layout.json
INGEST_TOKEN=change-me-ingest
LAB_AGENT_URL=http://192.168.100.50:9000
LAB_AGENT_TOKEN=change-me-agent
RECORD_EVENTS=0
LLM_ENABLED=0
ANTHROPIC_API_KEY=
LLM_MODEL=claude-haiku-4-5-20251001
ENV
cp .env.example .env

git add . && git commit -m "chore: bootstrap repository structure"
gh repo create rootiq --private --source=. --push     # أو أنشئه من الواجهة وأضف remote
```

### 🟦 FE — لوحة المهام
- GitHub Projects بأعمدة: `Backlog · Today · In Progress · Review · Done`.
- أنشئ Issue لكل مهمة من أيام هذا الملف بعنوان `[D03][FE] WebSocket client` وLabel للمسار.

### ⬜ ALL — `docs/CONTRACTS.md`
انسخ فيه الأقسام 2.1 → 2.6 حرفيًا. أي تغيير لاحق للعقد = PR مستقل يوافق عليه ممثل كل مسار.

### ✅ معايير قبول اليوم 0
- [ ] `git log --oneline | head -1` يطلع commit الـbootstrap على الريبو البعيد.
- [ ] `docs/CONTRACTS.md` موجود ومدموج.
- [ ] كل عضو سوّى `git clone` بنجاح.
- [ ] تاريخ يوم العرض مكتوب أعلى `README.md`.

---

# اليوم 1 — الأساس (Foundation)

**الهدف:** الواجهة ترسم الطوبولوجيا من ملف JSON، والباك إند يرد على `/api/health` و`/api/topology`، وEVE-NG جاهز بالصور.
**المخرجات:** `configs/topology.json` النهائي · مشروع Vite شغال · FastAPI + Postgres في Docker · مختبر فيه 5 عقد تقلع.

### ⬜ ALL — `configs/topology.json` (المصدر الوحيد للحقيقة)
```json
{
  "version": 1,
  "site": "RootIQ Lab",
  "vantage": "collector01",
  "nodes": [
    { "id": "r1", "type": "router", "label": "R1", "vendor": "Cisco vIOS", "managementIp": "10.10.10.1",
      "position": { "x": 420, "y": 40 },
      "interfaces": [
        { "name": "Gi0/0", "ifIndex": 1, "side": "bottom", "speedMbps": 10,   "description": "UPLINK-TO-SW1 (shaped 10M)" },
        { "name": "Gi0/1", "ifIndex": 2, "side": "bottom", "speedMbps": 1000, "description": "LINK-TO-SW2" }
      ] },
    { "id": "sw1", "type": "switch", "label": "SW1", "vendor": "Cisco vIOS-L2", "managementIp": "10.10.20.11",
      "position": { "x": 180, "y": 260 },
      "interfaces": [
        { "name": "Gi0/1", "ifIndex": 2, "side": "top",    "speedMbps": 1000 },
        { "name": "Gi0/3", "ifIndex": 4, "side": "bottom", "speedMbps": 1000 }
      ] },
    { "id": "sw2", "type": "switch", "label": "SW2", "vendor": "Cisco vIOS-L2", "managementIp": "10.10.30.12",
      "position": { "x": 660, "y": 260 },
      "interfaces": [
        { "name": "Gi0/1", "ifIndex": 2, "side": "top",    "speedMbps": 1000 },
        { "name": "Gi0/3", "ifIndex": 4, "side": "bottom", "speedMbps": 1000 }
      ] },
    { "id": "app01", "type": "server", "label": "APP-01", "vendor": "Ubuntu 24.04", "managementIp": "10.10.20.10",
      "position": { "x": 180, "y": 480 },
      "interfaces": [ { "name": "eth0", "side": "top", "speedMbps": 1000 } ] },
    { "id": "collector01", "type": "collector", "label": "COLLECTOR-01", "vendor": "Ubuntu 24.04", "managementIp": "10.10.30.10",
      "position": { "x": 660, "y": 480 },
      "interfaces": [ { "name": "ens3", "side": "top", "speedMbps": 1000 } ] }
  ],
  "links": [
    { "id": "link-r1-sw1",          "source": "r1",  "sourcePort": "Gi0/0", "target": "sw1",         "targetPort": "Gi0/1", "role": "uplink" },
    { "id": "link-r1-sw2",          "source": "r1",  "sourcePort": "Gi0/1", "target": "sw2",         "targetPort": "Gi0/1", "role": "uplink" },
    { "id": "link-sw1-app01",       "source": "sw1", "sourcePort": "Gi0/3", "target": "app01",       "targetPort": "eth0",  "role": "access" },
    { "id": "link-sw2-collector01", "source": "sw2", "sourcePort": "Gi0/3", "target": "collector01", "targetPort": "ens3",  "role": "access" }
  ],
  "services": [
    { "id": "svc-dns", "label": "Internal DNS",    "host": "app01", "port": 53, "dependsOn": [] },
    { "id": "svc-web", "label": "Web Application", "host": "app01", "port": 80, "dependsOn": ["svc-dns"] }
  ]
}
```
> ⚠️ قيم `ifIndex` مبدئية — 🟥 INFRA يثبتها في اليوم 3 بـ`snmpwalk` ويعدّلها هنا.

### 🟦 FE — مشروع React
```bash
cd ~/dev/rootiq
npm create vite@latest frontend -- --template react-ts
cd frontend
npm i @xyflow/react zustand react-router recharts motion lucide-react clsx i18next react-i18next
npm i -D tailwindcss @tailwindcss/vite vitest jsdom @testing-library/react @testing-library/jest-dom @playwright/test @types/node
```

**`frontend/vite.config.ts`**
```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@configs': path.resolve(__dirname, '../configs'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/ws': { target: 'ws://localhost:8000', ws: true },
    },
  },
  test: { environment: 'jsdom', globals: true },
});
```
> أضف في `tsconfig.app.json` داخل `compilerOptions`: `"baseUrl": ".", "paths": { "@/*": ["src/*"], "@configs/*": ["../configs/*"] }, "resolveJsonModule": true, "types": ["vitest/globals"]`

**`frontend/src/index.css`**
```css
@import "tailwindcss";

@theme {
  --color-noc-bg: #0b1020;
  --color-noc-panel: #111831;
  --color-noc-line: #1f2a4d;
  --color-ok: #22c55e;
  --color-warn: #eab308;
  --color-degraded: #f97316;
  --color-crit: #ef4444;
  --color-info: #38bdf8;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}

html, body, #root { height: 100%; }
body { @apply bg-noc-bg text-slate-100 antialiased; }

@keyframes rootiq-dash { to { stroke-dashoffset: -32; } }
.rootiq-flow { animation: rootiq-dash linear infinite; }
@keyframes rootiq-glow { 0%,100% { filter: drop-shadow(0 0 2px #ef4444); } 50% { filter: drop-shadow(0 0 12px #ef4444); } }
.rootiq-cause { animation: rootiq-glow 1.2s ease-in-out infinite; }
```

**`frontend/src/lib/types.ts`** (نسخة كاملة من العقد — لا تُعدّل إلا مع `docs/CONTRACTS.md`)
```ts
export type Health = 'healthy' | 'warning' | 'degraded' | 'critical' | 'unknown';
export type NodeType = 'router' | 'switch' | 'server' | 'collector';
export type Side = 'top' | 'bottom' | 'left' | 'right';

export interface Iface { name: string; ifIndex?: number; side: Side; speedMbps: number; description?: string;
  operState?: 'up' | 'down'; utilization?: number; }
export interface TopoNode { id: string; type: NodeType; label: string; vendor?: string; managementIp: string;
  position: { x: number; y: number }; interfaces: Iface[]; status: Health; metrics: Record<string, number>; }
export interface TopoLink { id: string; source: string; sourcePort: string; target: string; targetPort: string;
  role: 'uplink' | 'access' | 'backup'; speedMbps: number; status: Health;
  utilization: number; latencyMs: number; packetLoss: number; }
export interface Service { id: string; label: string; host: string; port: number; dependsOn: string[];
  status: Health; metrics: Record<string, number>; }
export interface Topology { site: string; vantage: string; nodes: TopoNode[]; links: TopoLink[]; services: Service[]; }

export type IncidentStatus = 'open' | 'investigating' | 'recommendation_ready' | 'awaiting_approval'
  | 'approved' | 'rejected' | 'resolved';
export type ScoreKey = 'metric_anomaly' | 'dependency_overlap' | 'temporal_proximity' | 'blast_radius' | 'historical_support';

export interface Evidence { id: string; entityId: string; metric: string; value: number; baseline: number;
  unit: string; ts: string; text: string; }
export interface Candidate { entityId: string; label: string; score: number; components: Record<ScoreKey, number>;
  evidence: string[]; suppressedBy?: string | null; }
export interface Action { id: string; incidentId: string; actionType: string; description: string;
  riskLevel: 'low' | 'medium' | 'high'; approvalStatus: 'pending' | 'approved' | 'rejected' | 'executed' | 'failed';
  decidedBy?: string; reason?: string; decidedAt?: string; executedAt?: string; }
export interface Incident {
  id: string; title: string; status: IncidentStatus; severity: 'low' | 'medium' | 'high' | 'critical';
  openedAt: string; resolvedAt?: string;
  rootCause?: { entityId: string; label: string; confidence: number };
  needsInvestigation: boolean;
  candidates: Candidate[]; evidence: Evidence[]; affectedServices: string[];
  causePath: string[]; impactPath: string[];
  explanation?: { en: string; ar: string; source: 'template' | 'llm' };
  action?: Action; rawAlertCount: number;
  timings: { injectedAt?: string; firstAnomalyAt?: string; detectedAt?: string; analyzedAt?: string;
             decidedAt?: string; executedAt?: string; recoveredAt?: string };
}
export interface RawAlert { id: string; sourceId: string; metric: string; value: number;
  severity: 'warning' | 'critical'; ts: string; }
export interface DemoState { mode: 'live' | 'sim'; scenario: string | null;
  state: 'idle' | 'injected' | 'remediating' | 'recovered'; injectedAt?: string; }
export interface Snapshot { topology: Topology; incidents: Incident[]; alerts: RawAlert[]; demo: DemoState; }

export type WsMessage =
  | { type: 'snapshot'; ts: number; data: Snapshot }
  | { type: 'link'; ts: number; data: Pick<TopoLink, 'id' | 'status' | 'utilization' | 'latencyMs' | 'packetLoss'> }
  | { type: 'node'; ts: number; data: { id: string; status: Health; metrics: Record<string, number> } }
  | { type: 'service'; ts: number; data: { id: string; status: Health; metrics: Record<string, number> } }
  | { type: 'alert'; ts: number; data: RawAlert }
  | { type: 'incident'; ts: number; data: Incident }
  | { type: 'demo'; ts: number; data: DemoState };
```

**`frontend/src/lib/staticTopology.ts`** (مؤقت لليوم 1–2 فقط)
```ts
import raw from '@configs/topology.json';
import type { Topology } from './types';

export const staticTopology: Topology = {
  site: raw.site, vantage: raw.vantage,
  nodes: raw.nodes.map((n) => ({ ...n, type: n.type as Topology['nodes'][number]['type'],
    interfaces: n.interfaces.map((i) => ({ ...i, side: i.side as 'top' })), status: 'healthy', metrics: {} })),
  links: raw.links.map((l) => ({ ...l, role: l.role as 'uplink', speedMbps: 1000, status: 'healthy',
    utilization: 0, latencyMs: 0, packetLoss: 0 })),
  services: raw.services.map((s) => ({ ...s, status: 'healthy', metrics: {} })),
};
```

**الهيكل العام:** أنشئ `src/components/layout/Shell.tsx` (CSS Grid: sidebar 72px يسار · topbar 56px · main · timeline 180px تحت) و`Sidebar.tsx` بعناصر الوثيقة: Topology · Incidents · Devices · Services · Analytics · Automation · Settings (أيقونات lucide: `Network, Siren, Server, Boxes, BarChart3, ShieldCheck, Settings`). و`App.tsx` بـReact Router:
```tsx
import { BrowserRouter, Routes, Route } from 'react-router';
import { Shell } from '@/components/layout/Shell';
import { OperationsPage } from '@/pages/OperationsPage';
// ... بقية الصفحات placeholders ترجع <div>Coming soon</div>

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Shell />}>
          <Route index element={<OperationsPage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="devices" element={<DevicesPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="audit" element={<AuditPage />} />
          <Route path="settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```
`OperationsPage` اليوم: `<ReactFlow>` بالعقد الافتراضية (بدون custom types) من `staticTopology` + `<Background />` + `<Controls />` + `fitView`. (لا تنسَ `import '@xyflow/react/dist/style.css'` في `main.tsx`.)

### 🟩 BE — FastAPI + Postgres
```bash
cd ~/dev/rootiq/backend
python3.12 -m venv .venv && source .venv/bin/activate
cat > requirements.txt << 'REQ'
fastapi>=0.115
uvicorn[standard]>=0.30
pydantic>=2.8
pydantic-settings>=2.4
sqlalchemy>=2.0
psycopg[binary]>=3.2
networkx>=3.3
numpy>=2.0
scikit-learn>=1.5
httpx>=0.27
pytest>=8.3
pytest-asyncio>=0.24
REQ
pip install -r requirements.txt
```

**`backend/app/core/config.py`**
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    rootiq_mode: str = "sim"
    database_url: str = "postgresql+psycopg://rootiq:rootiq@localhost:5432/rootiq"
    topology_path: str = "../configs/topology.json"
    layout_path: str = "../configs/layout.json"
    ingest_token: str = "change-me-ingest"
    lab_agent_url: str = "http://127.0.0.1:9000"
    lab_agent_token: str = "change-me-agent"
    record_events: bool = False
    llm_enabled: bool = False
    anthropic_api_key: str = ""
    llm_model: str = "claude-haiku-4-5-20251001"

settings = Settings()
```

**`backend/app/main.py`**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import health, topology

@asynccontextmanager
async def lifespan(app: FastAPI):
    # اليوم 3+: تحميل الطوبولوجيا، إنشاء الجداول، تشغيل المحاكي
    yield

app = FastAPI(title="RootIQ API", version="0.1.0", lifespan=lifespan)
app.include_router(health.router, prefix="/api")
app.include_router(topology.router, prefix="/api")
```

**`backend/app/api/health.py`**
```python
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok", "mode": settings.rootiq_mode}
```

**`backend/app/api/topology.py`** (نسخة اليوم 1: يرجع الملف كما هو)
```python
import json
from pathlib import Path
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["topology"])

@router.get("/topology")
def get_topology():
    return json.loads(Path(settings.topology_path).read_text(encoding="utf-8"))
```

**`backend/Dockerfile`**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`docker-compose.yml`** (الجذر)
```yaml
services:
  db:
    image: postgres:16
    environment: { POSTGRES_USER: rootiq, POSTGRES_PASSWORD: rootiq, POSTGRES_DB: rootiq }
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD-SHELL", "pg_isready -U rootiq"], interval: 5s, retries: 10 }
  backend:
    build: { context: ., dockerfile: backend/Dockerfile }
    env_file: .env
    ports: ["8000:8000"]
    volumes: ["./configs:/app/configs", "./data:/app/data"]
    depends_on: { db: { condition: service_healthy } }
volumes: { pgdata: {} }
```

**`scripts/dev.sh`** (تشغيل محلي سريع بدون بناء صور)
```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose up -d db
( cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000 ) &
( cd frontend && npm run dev ) &
wait
```
```bash
chmod +x scripts/dev.sh
```

### 🟨 AI — العتبات والرسم البياني المبدئي
- أنشئ `backend/app/intelligence/thresholds.py` يحوّل جدول 2.4 إلى كود:
```python
# (warning, critical, direction)  direction: "up" = الأعلى أسوأ، "down" = الأقل أسوأ
THRESHOLDS: dict[str, tuple[float, float, str]] = {
    "link_utilization": (70, 85, "up"),
    "link_latency_ms": (30, 60, "up"),
    "link_packet_loss": (1, 5, "up"),
    "if_out_discards_rate": (5, 50, "up"),
    "if_oper_status": (0.5, 0.5, "down"),
    "cpu_percent": (80, 95, "up"),
    "mem_percent": (85, 95, "up"),
    "http_latency_ms": (300, 1000, "up"),
    "http_ok": (0.5, 0.5, "down"),
    "dns_success_rate": (95, 50, "down"),
    "dns_latency_ms": (100, 500, "up"),
}

def static_severity(metric: str, value: float) -> float:
    """0 = طبيعي، 0.5 = warning، 1.0 = critical"""
    if metric not in THRESHOLDS:
        return 0.0
    warn, crit, direction = THRESHOLDS[metric]
    if direction == "up":
        return 1.0 if value >= crit else 0.5 if value >= warn else 0.0
    return 1.0 if value <= crit else 0.5 if value < warn else 0.0
```
- اكتب `backend/tests/test_thresholds.py` بـ6 حالات على الأقل (قيمة طبيعية/تحذير/حرجة لـ`link_utilization` و`dns_success_rate`).

### 🟥 INFRA — EVE-NG والصور
```bash
# على جهاز EVE-NG
uname -a && free -g && nproc          # تأكد من ≥16GB RAM
mkdir -p /opt/unetlab/addons/qemu/vios-adventerprisek9-m.SPA.159-3.M
mkdir -p /opt/unetlab/addons/qemu/viosl2-adventerprisek9-m.SSA.high_iron
mkdir -p /opt/unetlab/addons/qemu/linux-ubuntu-24.04-server
# انسخ virtioa.qcow2 لكل مجلد (scp من جهازك) ثم:
/opt/unetlab/wrappers/unl_wrapper -a fixpermissions
```
- أنشئ Lab اسمه `rootiq` فيه: R1 (vIOS, 1GB) · SW1/SW2 (vIOS-L2, 1GB) · APP-01 (Ubuntu, 2GB, 2 vCPU) · COLLECTOR-01 (Ubuntu, 2GB, 2 vCPU) · Cloud0 (management → ens4 للكولكتر) · NAT (مؤقت لتثبيت الحزم على APP-01).
- وصّل الروابط **بالضبط** كما في 2.1.
- صدّر المختبر إلى `lab/eve/rootiq.unl` وارفعه للريبو.

### ✅ معايير قبول اليوم 1
- [ ] `docker compose up -d db && docker compose ps` → `db` بحالة `healthy`.
- [ ] `curl -s localhost:8000/api/health` → `{"status":"ok","mode":"sim"}`
- [ ] `curl -s localhost:8000/api/topology | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d['nodes']),len(d['links']))"` → `5 4`
- [ ] `cd frontend && npx tsc -b --noEmit && npm run build` بدون أخطاء.
- [ ] `http://localhost:5173` يعرض 5 عقد و4 روابط + Sidebar بـ7 عناصر.
- [ ] `cd backend && pytest -q` → كل اختبارات العتبات تنجح.
- [ ] العقد الخمس في EVE-NG تقلع وتقدر تفتح console لكل وحدة.
- [ ] `git tag day-01 && git push --tags`

---

# اليوم 2 — الطوبولوجيا الحقيقية (Custom Nodes + منافذ حقيقية)

**الهدف:** الخريطة تصير «Graph» حقيقي: كل رابط مربوط بمنفذ حقيقي على الجهاز، واسم المنفذين على الرابط، والتخطيط يُحفظ.
**المخرجات:** `DeviceNode` · `PortEdge` · Inspectors · API للتخطيط · `graph.py` بالمسارات · إعدادات الأجهزة في المختبر.

### 🟦 FE — العقد والروابط المخصصة

**`frontend/src/lib/colors.ts`**
```ts
import type { Health } from './types';
export const STATUS_COLOR: Record<Health, string> = {
  healthy: '#22c55e', warning: '#eab308', degraded: '#f97316', critical: '#ef4444', unknown: '#64748b',
};
export const CAUSE_COLOR = '#ef4444';
export const IMPACT_COLOR = '#f59e0b';
export const BACKUP_COLOR = '#38bdf8';
```

**`frontend/src/components/topology/DeviceNode.tsx`**
```tsx
import { Handle, Position, type Node, type NodeProps } from '@xyflow/react';
import { Router, Network, Server, Radar } from 'lucide-react';
import clsx from 'clsx';
import type { Iface, Side, TopoNode } from '@/lib/types';
import { STATUS_COLOR } from '@/lib/colors';

export type Focus = 'cause' | 'impact' | null;
export type DeviceNodeT = Node<{ device: TopoNode; focus: Focus }, 'device'>;

const ICON = { router: Router, switch: Network, server: Server, collector: Radar } as const;
const POS: Record<Side, Position> = { top: Position.Top, bottom: Position.Bottom, left: Position.Left, right: Position.Right };

function handleStyle(side: Side, idx: number, total: number): React.CSSProperties {
  const pct = `${((idx + 1) / (total + 1)) * 100}%`;
  return side === 'top' || side === 'bottom' ? { left: pct } : { top: pct };
}

export function DeviceNode({ data, selected }: NodeProps<DeviceNodeT>) {
  const { device, focus } = data;
  const Icon = ICON[device.type];
  const bySide = device.interfaces.reduce<Record<Side, Iface[]>>(
    (acc, i) => { (acc[i.side] ??= []).push(i); return acc; },
    {} as Record<Side, Iface[]>,
  );
  return (
    <div
      className={clsx(
        'min-w-[160px] rounded-xl border-2 bg-noc-panel/95 px-4 py-3 shadow-lg transition-colors',
        selected && 'ring-2 ring-info',
        focus === 'cause' && 'rootiq-cause',
      )}
      style={{ borderColor: focus === 'cause' ? '#ef4444' : focus === 'impact' ? '#f59e0b' : STATUS_COLOR[device.status] }}
    >
      <div className="flex items-center gap-2">
        <Icon className="size-5" style={{ color: STATUS_COLOR[device.status] }} />
        <span className="font-semibold tracking-wide">{device.label}</span>
      </div>
      <div className="mt-1 font-mono text-[11px] text-slate-400">{device.managementIp}</div>
      {(Object.keys(bySide) as Side[]).flatMap((side) =>
        bySide[side].map((i, idx) => (
          <Handle key={i.name} id={i.name} type="source" position={POS[side]}
            style={handleStyle(side, idx, bySide[side].length)}
            className="!size-2.5 !border-0 !bg-slate-300" title={i.name} />
        )),
      )}
    </div>
  );
}
```

**`frontend/src/components/topology/PortEdge.tsx`**
```tsx
import { BaseEdge, EdgeLabelRenderer, getSmoothStepPath, type Edge, type EdgeProps } from '@xyflow/react';
import type { TopoLink } from '@/lib/types';
import { CAUSE_COLOR, IMPACT_COLOR, STATUS_COLOR } from '@/lib/colors';
import type { Focus } from './DeviceNode';

export type PortEdgeT = Edge<{ link: TopoLink; focus: Focus }, 'port'>;

export function PortEdge(p: EdgeProps<PortEdgeT>) {
  const [path, lx, ly] = getSmoothStepPath({ ...p, borderRadius: 18 });
  const link = p.data!.link;
  const focus = p.data!.focus;
  const color = focus === 'cause' ? CAUSE_COLOR : focus === 'impact' ? IMPACT_COLOR : STATUS_COLOR[link.status];
  const width = 2 + Math.min(6, link.utilization / 18);
  const cycle = Math.max(0.35, 3 - link.utilization / 35);   // كل ما زاد الحمل زادت سرعة الحركة

  return (
    <>
      <BaseEdge id={p.id} path={path} style={{ stroke: color, strokeWidth: width, opacity: 0.35 }} />
      <path d={path} fill="none" stroke={color} strokeWidth={width} strokeDasharray="6 10"
        className={focus === 'cause' ? 'rootiq-flow rootiq-cause' : 'rootiq-flow'}
        style={{ animationDuration: `${cycle}s` }} />
      <EdgeLabelRenderer>
        <div
          className="nodrag nopan absolute rounded-md border bg-noc-bg/95 px-2 py-1 font-mono text-[11px] leading-tight"
          style={{ transform: `translate(-50%,-50%) translate(${lx}px,${ly}px)`, borderColor: color, pointerEvents: 'all' }}
        >
          <div>{link.sourcePort} ⇄ {link.targetPort}</div>
          <div className="text-slate-400">
            {Math.round(link.utilization)}% · {link.latencyMs.toFixed(0)} ms
            {link.packetLoss > 0 && <span className="text-crit"> · loss {link.packetLoss.toFixed(1)}%</span>}
          </div>
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
```

**`frontend/src/lib/layout.ts`**
```ts
import type { DeviceNodeT, Focus } from '@/components/topology/DeviceNode';
import type { PortEdgeT } from '@/components/topology/PortEdge';
import type { Topology } from './types';

export function toFlow(t: Topology, focus: Record<string, Focus> = {}) {
  const nodes: DeviceNodeT[] = t.nodes.map((n) => ({
    id: n.id, type: 'device', position: n.position, data: { device: n, focus: focus[n.id] ?? null },
  }));
  const edges: PortEdgeT[] = t.links.map((l) => ({
    id: l.id, type: 'port', source: l.source, target: l.target,
    sourceHandle: l.sourcePort, targetHandle: l.targetPort,
    data: { link: l, focus: focus[l.id] ?? null },
  }));
  return { nodes, edges };
}
```

**`frontend/src/components/topology/TopologyCanvas.tsx`**
```tsx
import { useEffect, useMemo } from 'react';
import { ReactFlow, Background, Controls, MiniMap, ConnectionMode, useNodesState } from '@xyflow/react';
import { DeviceNode, type DeviceNodeT, type Focus } from './DeviceNode';
import { PortEdge } from './PortEdge';
import { toFlow } from '@/lib/layout';
import type { Topology } from '@/lib/types';

// ⚠️ خارج الكومبوننت — لو داخله React Flow يعيد رسم كل شي كل render
const nodeTypes = { device: DeviceNode };
const edgeTypes = { port: PortEdge };
const NO_FOCUS: Record<string, Focus> = {};   // ثابت: لو `{}` افتراضي جديد كل render → حلقة لا نهائية

interface Props {
  topology: Topology;
  focus?: Record<string, Focus>;
  onSelect?: (sel: { kind: 'node' | 'link'; id: string } | null) => void;
  onLayoutSaved?: (positions: Record<string, { x: number; y: number }>) => void;
}

export function TopologyCanvas({ topology, focus = NO_FOCUS, onSelect, onLayoutSaved }: Props) {
  const flow = useMemo(() => toFlow(topology, focus), [topology, focus]);
  const [nodes, setNodes, onNodesChange] = useNodesState<DeviceNodeT>(flow.nodes);

  // دمج البيانات الحية مع الحفاظ على المواقع اللي سحبها المستخدم
  useEffect(() => {
    setNodes((cur) => flow.nodes.map((n) => ({ ...n, position: cur.find((c) => c.id === n.id)?.position ?? n.position })));
  }, [flow.nodes, setNodes]);

  return (
    <div dir="ltr" className="h-full w-full">   {/* الخريطة دايمًا LTR حتى لو الواجهة عربية */}
      <ReactFlow
        nodes={nodes} edges={flow.edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes}
        onNodesChange={onNodesChange} connectionMode={ConnectionMode.Loose}
        nodesConnectable={false} fitView minZoom={0.4} maxZoom={2}
        onNodeClick={(_, n) => onSelect?.({ kind: 'node', id: n.id })}
        onEdgeClick={(_, e) => onSelect?.({ kind: 'link', id: e.id })}
        onPaneClick={() => onSelect?.(null)}
        onNodeDragStop={(_, dragged) => onLayoutSaved?.({
          ...Object.fromEntries(nodes.map((n) => [n.id, n.position])), [dragged.id]: dragged.position })}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1f2a4d" gap={24} />
        <MiniMap pannable zoomable className="!bg-noc-panel" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
```

**Inspectors:** `LinkInspector.tsx` و`DeviceInspector.tsx` كـDrawer يمين (عرض 360px) يفتح عند الاختيار:
- الرابط: المصدر/الهدف + المنافذ + السرعة + الحالة + Utilization + Latency + Loss + «آخر الأحداث» (فاضية اليوم).
- الجهاز: النوع · الـVendor · IP · جدول المنافذ (الاسم، الحالة، السرعة، الاستخدام) · الخدمات المستضافة.

**اختبار الربط بالمنافذ — `frontend/src/lib/layout.test.ts`**
```ts
import { toFlow } from './layout';
import { staticTopology } from './staticTopology';

test('كل رابط مربوط بالمنفذ الصحيح', () => {
  const { edges } = toFlow(staticTopology);
  const e = edges.find((x) => x.id === 'link-r1-sw1')!;
  expect(e.sourceHandle).toBe('Gi0/0');
  expect(e.targetHandle).toBe('Gi0/1');
});

test('كل منفذ في رابط موجود فعلًا على الجهاز', () => {
  for (const l of staticTopology.links) {
    const s = staticTopology.nodes.find((n) => n.id === l.source)!;
    const t = staticTopology.nodes.find((n) => n.id === l.target)!;
    expect(s.interfaces.map((i) => i.name)).toContain(l.sourcePort);
    expect(t.interfaces.map((i) => i.name)).toContain(l.targetPort);
  }
});
```
أضف في `package.json`: `"test": "vitest run"`.

### 🟩 BE — خدمة الطوبولوجيا بحالة حيّة
**`backend/app/services/topology_service.py`**
```python
import json, os, tempfile
from pathlib import Path
from app.core.config import settings

class TopologyError(RuntimeError): ...

class TopologyService:
    def __init__(self):
        self.raw = json.loads(Path(settings.topology_path).read_text(encoding="utf-8"))
        self._validate()
        self.nodes = {n["id"]: n for n in self.raw["nodes"]}
        self.links = {l["id"]: l for l in self.raw["links"]}
        self.services = {s["id"]: s for s in self.raw["services"]}
        # (device, interface) -> link id — نستخدمه لترجمة عدّادات SNMP إلى رابط
        self.port_to_link = {}
        for l in self.links.values():
            self.port_to_link[(l["source"], l["sourcePort"])] = l["id"]
            self.port_to_link[(l["target"], l["targetPort"])] = l["id"]
        self._apply_layout()

    def _validate(self):
        ids = {n["id"]: {i["name"] for i in n["interfaces"]} for n in self.raw["nodes"]}
        for l in self.raw["links"]:
            for end, port in ((l["source"], l["sourcePort"]), (l["target"], l["targetPort"])):
                if end not in ids or port not in ids[end]:
                    raise TopologyError(f"link {l['id']}: unknown endpoint {end}:{port}")
        for s in self.raw["services"]:
            if s["host"] not in ids:
                raise TopologyError(f"service {s['id']}: unknown host {s['host']}")

    def _apply_layout(self):
        p = Path(settings.layout_path)
        if p.exists():
            for nid, pos in json.loads(p.read_text()).items():
                if nid in self.nodes:
                    self.nodes[nid]["position"] = pos

    def save_layout(self, positions: dict[str, dict]):
        unknown = set(positions) - set(self.nodes)
        if unknown:
            raise TopologyError(f"unknown nodes: {sorted(unknown)}")
        for nid, pos in positions.items():
            self.nodes[nid]["position"] = {"x": float(pos["x"]), "y": float(pos["y"])}
        fd, tmp = tempfile.mkstemp(dir=Path(settings.layout_path).parent)
        with os.fdopen(fd, "w") as f:
            json.dump({k: v["position"] for k, v in self.nodes.items()}, f, indent=2)
        os.replace(tmp, settings.layout_path)          # كتابة ذرّية: ما يخرب الملف لو انقطع

    def speed_of(self, link_id: str) -> int:
        l = self.links[link_id]
        src = next(i for i in self.nodes[l["source"]]["interfaces"] if i["name"] == l["sourcePort"])
        return src["speedMbps"]
```
- عدّل `api/topology.py`: `GET /api/topology` يرجع العقد (بمواقعها) + الروابط مع `speedMbps` + الخدمات + حالة افتراضية `healthy`؛ و`PUT /api/topology/layout` يستقبل `{ "positions": { "r1": {"x":..,"y":..} } }` ويرجع 400 لأي id مجهول؛ و`GET /api/devices/{id}` يرجع 404 للمجهول.
- في `lifespan` أنشئ `app.state.topology = TopologyService()` — لو فيه خطأ في الملف السيرفر **يرفض يقلع** (Fail fast).

### 🟨 AI — `graph.py` (قلب الاستدلال الطوبولوجي)
**`backend/app/intelligence/graph.py`**
```python
import networkx as nx

class TopologyGraph:
    """الأجهزة والروابط كلها عقد في الرسم؛ الروابط عقد وسيطة حتى يظهر id الرابط داخل المسار."""
    def __init__(self, topo: dict):
        self.g = nx.Graph()
        self.vantage = topo["vantage"]
        for n in topo["nodes"]:
            self.g.add_node(n["id"], kind="device", label=n["label"])
        for l in topo["links"]:
            self.g.add_node(l["id"], kind="link", label=f'{l["source"].upper()} {l["sourcePort"]} → {l["target"].upper()} {l["targetPort"]}')
            self.g.add_edge(l["source"], l["id"])
            self.g.add_edge(l["id"], l["target"])
        self.services = {s["id"]: s for s in topo["services"]}
        for s in self.services.values():
            self.g.add_node(s["id"], kind="service", label=s["label"])
        self._paths = {sid: self._path(sid) for sid in self.services}

    def _path(self, sid: str) -> list[str]:
        s = self.services[sid]
        chain = nx.shortest_path(self.g, self.vantage, s["host"])
        deps: list[str] = []
        for d in s.get("dependsOn", []):
            for x in self._path(d):
                if x not in chain and x not in deps:
                    deps.append(x)
        return chain + deps + [sid]

    def service_dependencies(self, sid: str) -> list[str]:
        return self._paths[sid]

    def downstream(self, x: str) -> set[str]:
        out: set[str] = set()
        for p in self._paths.values():
            if x in p:
                out |= set(p[p.index(x) + 1:])
        return out

    def upstream(self, x: str) -> set[str]:
        out: set[str] = set()
        for p in self._paths.values():
            if x in p:
                out |= set(p[: p.index(x)])
        return out

    def services_through(self, x: str) -> list[str]:
        return [sid for sid, p in self._paths.items() if x in p]

    def label(self, x: str) -> str:
        return self.g.nodes[x]["label"]

    def hop_distance(self, a: str, b: str) -> int:
        if a in self.services or b in self.services:
            return 0 if (a in self.downstream(b) or b in self.downstream(a) or a == b) else 99
        return nx.shortest_path_length(self.g, a, b)
```
**`backend/tests/test_graph.py`**
```python
import json
from pathlib import Path
from app.intelligence.graph import TopologyGraph

TOPO = json.loads(Path(__file__).resolve().parents[2].joinpath("configs/topology.json").read_text())
g = TopologyGraph(TOPO)

def test_web_path_crosses_uplink_and_dns():
    p = g.service_dependencies("svc-web")
    assert p[0] == "collector01" and p[-1] == "svc-web"
    assert "link-r1-sw1" in p and "svc-dns" in p

def test_dns_is_downstream_of_uplink():
    assert {"svc-dns", "svc-web", "app01"} <= g.downstream("link-r1-sw1")

def test_uplink_is_upstream_of_dns():
    assert "link-r1-sw1" in g.upstream("svc-dns")

def test_collector_access_link_not_downstream_of_uplink():
    assert "link-sw2-collector01" not in g.downstream("link-r1-sw1")
```

### 🟥 INFRA — إعداد الأجهزة
**`lab/configs/r1.cfg`**
```text
hostname R1
ip domain name rootiq.lab
username rootiq privilege 15 secret RootIQ-Lab-2026
ip ssh version 2
!
ip access-list extended BULK-TRAFFIC
 permit udp any any eq 5201
 permit tcp any any eq 5201
 permit tcp any eq 5201 any
class-map match-any BULK
 match access-group name BULK-TRAFFIC
policy-map CHILD-QOS
 class BULK
  police 2000000 conform-action transmit exceed-action drop
 class class-default
  fair-queue
policy-map UPLINK-SHAPE
 class class-default
  shape average 10000000
policy-map UPLINK-QOS
 class class-default
  shape average 10000000
  service-policy CHILD-QOS
!
interface Loopback0
 ip address 10.10.10.1 255.255.255.255
interface GigabitEthernet0/0
 description UPLINK-TO-SW1-Gi0/1
 bandwidth 10000
 ip address 10.10.20.1 255.255.255.0
 service-policy output UPLINK-SHAPE
 no shutdown
interface GigabitEthernet0/1
 description LINK-TO-SW2-Gi0/1
 ip address 10.10.30.1 255.255.255.0
 no shutdown
!
snmp-server community rootiq-ro RO
snmp-server ifindex persist
logging host 10.10.30.10
logging trap informational
cdp run
lldp run
line vty 0 4
 login local
 transport input ssh
end
```
بعد اللصق نفّذ مرة وحدة: `crypto key generate rsa modulus 2048` ثم `write memory`.

**`lab/configs/sw1.cfg`** (وSW2 نفسه مع `10.10.30.12` وgw `10.10.30.1` والوصف المناسب)
```text
hostname SW1
interface GigabitEthernet0/1
 description TO-R1-Gi0/0
 switchport mode access
interface GigabitEthernet0/3
 description TO-APP-01-eth0
 switchport mode access
interface Vlan1
 ip address 10.10.20.11 255.255.255.0
 no shutdown
ip default-gateway 10.10.20.1
! لو الصورة مفعّل فيها ip routing استخدم بدلها:
! ip route 0.0.0.0 0.0.0.0 10.10.20.1
snmp-server community rootiq-ro RO
logging host 10.10.30.10
cdp run
lldp run
end
```

**APP-01 — `/etc/netplan/01-lab.yaml`** (وCOLLECTOR-01 نفسه بـ`ens3: 10.10.30.10/24 via 10.10.30.1` + `ens4: dhcp4: true`)
```yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [10.10.20.10/24]
      routes: [{ to: default, via: 10.10.20.1 }]
      nameservers: { addresses: [10.10.20.10] }
```
```bash
sudo netplan apply
```

### ✅ معايير قبول اليوم 2
- [ ] `npm test` في `frontend` → اختبارا الربط بالمنافذ ✅.
- [ ] على الشاشة: كل رابط يخرج من نقطة المنفذ الصحيحة وعليه `Gi0/0 ⇄ Gi0/1` إلخ.
- [ ] الضغط على جهاز يفتح DeviceInspector بجدول منافذه؛ الضغط على رابط يفتح LinkInspector.
- [ ] اسحب R1 ← `curl -s localhost:8000/api/topology | grep -A2 '"r1"'` يعكس الموقع الجديد، وبعد إعادة تشغيل الباك إند الموقع باقٍ.
- [ ] `curl -s -X PUT localhost:8000/api/topology/layout -H 'content-type: application/json' -d '{"positions":{"zz":{"x":1,"y":1}}}' -o /dev/null -w '%{http_code}'` → `400`
- [ ] `pytest -q tests/test_graph.py` → 4 passed.
- [ ] من COLLECTOR-01: `traceroute -n 10.10.20.10` → القفزة الأولى `10.10.30.1` والثانية `10.10.20.10`.
- [ ] على R1: `show policy-map interface Gi0/0` يظهر `UPLINK-SHAPE` · `show cdp neighbors` يظهر SW1 وSW2.
- [ ] `git tag day-02`

---

# اليوم 3 — خط البيانات الحي (Event → State → WebSocket → Map)

**الهدف:** أي حدث يدخل `POST /api/events` يظهر على الخريطة خلال ≤ 1 ثانية بدون Refresh. وضع المحاكاة يولّد حالة «طبيعية» حيّة (أرقام تتذبذب بشكل واقعي).
**المخرجات:** Schemas · Hub · StateStore · Simulator · WS · Zustand store · Sparklines · خدمات APP-01.

### 🟩 BE — Schemas والـHub والحالة
**`backend/app/schemas/common.py`**
```python
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
```
**`backend/app/schemas/event.py`**
```python
from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import Field
from .common import CamelModel

SourceType = Literal["router", "switch", "server", "collector", "link", "service"]

class Event(CamelModel):
    event_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_id: str
    source_type: SourceType
    metric: str
    value: float
    unit: str
    interface: str | None = None
    severity: Literal["info", "warning", "critical"] = "info"
    metadata: dict[str, Any] = Field(default_factory=dict)

class EventBatch(CamelModel):
    events: list[Event] = Field(max_length=500)
```
**`backend/app/services/hub.py`**
```python
import json, time
from fastapi import WebSocket

class Hub:
    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)

    def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)

    async def send(self, ws: WebSocket, type_: str, data):
        await ws.send_text(json.dumps({"type": type_, "ts": time.time(), "data": data}, default=str))

    async def broadcast(self, type_: str, data):
        msg = json.dumps({"type": type_, "ts": time.time(), "data": data}, default=str)
        for c in list(self.clients):
            try:
                await c.send_text(msg)
            except Exception:
                self.clients.discard(c)

hub = Hub()
```
**`backend/app/services/state_store.py`** (الحالة الحالية + تاريخ قصير في الذاكرة + بث مخنوق 1Hz)
```python
import asyncio
from collections import defaultdict, deque
from app.intelligence.thresholds import static_severity
from app.services.hub import hub

LINK_FIELDS = {"link_utilization": "utilization", "link_latency_ms": "latencyMs", "link_packet_loss": "packetLoss"}

def sev_to_status(sev: float) -> str:
    return "critical" if sev >= 1 else "warning" if sev >= 0.5 else "healthy"

class StateStore:
    def __init__(self, topo):
        self.topo = topo
        self.metrics: dict[str, dict[str, float]] = defaultdict(dict)                 # entity -> metric -> value
        self.history: dict[str, deque] = defaultdict(lambda: deque(maxlen=300))       # "entity|metric" -> (ts, v)
        self.dirty: set[str] = set()

    def kind(self, entity: str) -> str:
        if entity in self.topo.links: return "link"
        if entity in self.topo.services: return "service"
        return "node"

    def update(self, source_id: str, metric: str, value: float, ts: float):
        self.metrics[source_id][metric] = value
        self.history[f"{source_id}|{metric}"].append((ts, value))
        self.dirty.add(source_id)

    def status(self, entity: str) -> str:
        return sev_to_status(max((static_severity(m, v) for m, v in self.metrics[entity].items()), default=0))

    def payload(self, entity: str) -> dict:
        m = self.metrics[entity]
        if self.kind(entity) == "link":
            return {"id": entity, "status": self.status(entity),
                    **{camel: round(m.get(k, 0.0), 2) for k, camel in LINK_FIELDS.items()}}
        return {"id": entity, "status": self.status(entity), "metrics": {k: round(v, 2) for k, v in m.items()}}

    async def flush_loop(self):
        while True:
            await asyncio.sleep(1.0)
            dirty, self.dirty = self.dirty, set()
            for e in dirty:
                await hub.broadcast(self.kind(e), self.payload(e))
```
**`backend/app/services/pipeline.py`** (نسخة اليوم 3 — نوسّعها يوم 5 و6)
```python
from fastapi import HTTPException
from app.schemas.event import Event

class Pipeline:
    def __init__(self, topo, state):
        self.topo, self.state = topo, state
        self.known = set(topo.nodes) | set(topo.links) | set(topo.services)

    async def ingest(self, ev: Event):
        # ترجمة عدّاد منفذ جهاز إلى رابط: (r1, Gi0/0) -> link-r1-sw1
        if ev.source_type in ("router", "switch") and ev.interface and ev.metric.startswith(("link_", "if_")):
            link = self.topo.port_to_link.get((ev.source_id, ev.interface))
            if link:
                ev.source_id, ev.source_type = link, "link"
        if ev.source_id not in self.known:
            raise HTTPException(422, f"unknown sourceId {ev.source_id}")   # ضابط أمان من الوثيقة
        self.state.update(ev.source_id, ev.metric, ev.value, ev.timestamp.timestamp())
```
**`backend/app/api/events.py`**
```python
from fastapi import APIRouter, Header, HTTPException, Request
from app.core.config import settings
from app.schemas.event import Event, EventBatch

router = APIRouter(tags=["events"])

def _auth(token: str | None):
    if token != settings.ingest_token:
        raise HTTPException(401, "bad ingest token")

@router.post("/events", status_code=202)
async def post_event(ev: Event, request: Request, x_rootiq_token: str | None = Header(None)):
    _auth(x_rootiq_token)
    await request.app.state.pipeline.ingest(ev)
    return {"accepted": 1}

@router.post("/events/batch", status_code=202)
async def post_batch(batch: EventBatch, request: Request, x_rootiq_token: str | None = Header(None)):
    _auth(x_rootiq_token)
    for ev in batch.events:
        await request.app.state.pipeline.ingest(ev)
    return {"accepted": len(batch.events)}
```
**`backend/app/api/ws.py`**
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.hub import hub

router = APIRouter()

@router.websocket("/ws/operations")
async def operations(ws: WebSocket):
    await hub.connect(ws)
    await hub.send(ws, "snapshot", ws.app.state.snapshot())
    try:
        while True:
            await ws.receive_text()           # نتجاهل أي رسائل؛ فقط نبقي الاتصال
    except WebSocketDisconnect:
        hub.disconnect(ws)
```
- `app.state.snapshot()` = دالة في `main.py` ترجع `{topology (مع حالة كل رابط/جهاز/خدمة من state.payload), incidents: [], alerts: [], demo: {...}}`.
- أضف `GET /api/links/{id}/metrics?minutes=5` يرجع `{utilization:[[ts,v]...], latencyMs:[...], packetLoss:[...]}` من `state.history`.
- في `lifespan`: أنشئ `topo, state, pipeline`، و`asyncio.create_task(state.flush_loop())`، ولو `ROOTIQ_MODE=sim` شغّل `asyncio.create_task(simulator.run())`. سجّل `ws.router` بدون prefix.

**`backend/app/collectors/simulator.py`** (محرك المحاكاة الكامل — السيناريوهات تُفعّل يوم 5)
```python
import asyncio, random
from datetime import datetime, timezone
from app.schemas.event import Event

# (entity, sourceType, metric, unit, baseline, noise)
BASELINE = [
    ("link-r1-sw1", "link", "link_utilization", "percent", 14, 3),
    ("link-r1-sw1", "link", "link_latency_ms", "ms", 2.5, 0.6),
    ("link-r1-sw1", "link", "link_packet_loss", "percent", 0, 0),
    ("link-r1-sw1", "link", "if_out_discards_rate", "pps", 0, 0),
    ("link-r1-sw2", "link", "link_utilization", "percent", 6, 2),
    ("link-r1-sw2", "link", "link_latency_ms", "ms", 1.2, 0.3),
    ("link-sw1-app01", "link", "link_utilization", "percent", 9, 2),
    ("link-sw1-app01", "link", "link_latency_ms", "ms", 0.8, 0.2),
    ("link-sw2-collector01", "link", "link_utilization", "percent", 5, 1),
    ("app01", "server", "cpu_percent", "percent", 18, 4),
    ("app01", "server", "mem_percent", "percent", 41, 1),
    ("svc-web", "service", "http_latency_ms", "ms", 42, 8),
    ("svc-web", "service", "http_ok", "bool", 1, 0),
    ("svc-dns", "service", "dns_success_rate", "percent", 100, 0),
    ("svc-dns", "service", "dns_latency_ms", "ms", 4, 1),
]
# scenario -> [(offset_s, entity, metric, target, ramp_s)]
SCENARIOS = {
    "uplink-congestion": [
        (0, "link-r1-sw1", "link_utilization", 97, 4), (1, "link-r1-sw1", "if_out_discards_rate", 180, 4),
        (2, "link-r1-sw1", "link_latency_ms", 86, 6), (3, "link-r1-sw1", "link_packet_loss", 2.4, 6),
        (6, "svc-web", "http_latency_ms", 1450, 6), (8, "svc-dns", "dns_success_rate", 72, 5),
        (8, "svc-dns", "dns_latency_ms", 620, 5),
    ],
    "dns-failure": [
        (0, "svc-dns", "dns_success_rate", 0, 2), (0, "svc-dns", "dns_latency_ms", 1000, 2),
        (2, "svc-web", "http_ok", 0, 1),
    ],
    "server-spike": [
        (0, "app01", "cpu_percent", 98, 5), (1, "app01", "mem_percent", 78, 8),
        (4, "svc-web", "http_latency_ms", 1100, 6), (6, "svc-dns", "dns_latency_ms", 160, 6),
    ],
}

class Simulator:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.current = {(e, m): b for e, _, m, _, b, _ in BASELINE}
        self.active: str | None = None
        self.elapsed = 0.0
        self.recovering = False

    def inject(self, scenario: str):
        assert scenario in SCENARIOS
        self.active, self.elapsed, self.recovering = scenario, 0.0, False

    def remediate(self):
        self.recovering = True

    def reset(self):
        self.active, self.recovering = None, False
        self.current = {(e, m): b for e, _, m, _, b, _ in BASELINE}

    def _target(self, e, m, base):
        if not self.active or self.recovering:
            return base, 8.0
        for off, te, tm, tgt, ramp in SCENARIOS[self.active]:
            if te == e and tm == m and self.elapsed >= off:
                return tgt, ramp
        return base, 4.0

    async def run(self, tick: float = 1.0):
        while True:
            await asyncio.sleep(tick)
            self.elapsed += tick
            now = datetime.now(timezone.utc)
            for e, st, m, unit, base, noise in BASELINE:
                tgt, ramp = self._target(e, m, base)
                cur = self.current[(e, m)]
                cur += (tgt - cur) * min(1.0, tick / ramp)
                self.current[(e, m)] = cur
                val = max(0.0, cur + random.gauss(0, noise))
                if unit == "percent":
                    val = min(val, 100.0)
                if unit == "bool":
                    val = 1.0 if cur >= 0.5 else 0.0
                await self.pipeline.ingest(Event(source_id=e, source_type=st, metric=m, value=round(val, 2),
                                                 unit=unit, timestamp=now, metadata={"collector": "simulator"}))
```

### 🟦 FE — WebSocket + Store
**`frontend/src/lib/ws.ts`**
```ts
import type { WsMessage } from './types';
export type WsStatus = 'connecting' | 'open' | 'closed';

export function connectOps(onMessage: (m: WsMessage) => void, onStatus: (s: WsStatus) => void) {
  let ws: WebSocket | null = null;
  let retry = 0;
  let stopped = false;
  const url = `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws/operations`;

  const open = () => {
    onStatus('connecting');
    ws = new WebSocket(url);
    ws.onopen = () => { retry = 0; onStatus('open'); };
    ws.onmessage = (e) => onMessage(JSON.parse(e.data) as WsMessage);
    ws.onclose = () => {
      onStatus('closed');
      if (!stopped) setTimeout(open, Math.min(5000, 500 * 2 ** retry++));   // backoff: 0.5s → 5s
    };
  };
  open();
  return () => { stopped = true; ws?.close(); };
}
```
**`frontend/src/store/useOps.ts`**
```ts
import { create } from 'zustand';
import type { DemoState, Incident, RawAlert, Topology, WsMessage } from '@/lib/types';
import type { WsStatus } from '@/lib/ws';

type Point = { t: number; util: number; lat: number; loss: number };
export type Selection = { kind: 'node' | 'link' | 'incident'; id: string } | null;

interface OpsState {
  topology: Topology | null;
  linkHistory: Record<string, Point[]>;
  incidents: Record<string, Incident>;
  alerts: RawAlert[];
  demo: DemoState;
  wsStatus: WsStatus;
  lastUpdate: number;
  selection: Selection;
  apply: (m: WsMessage) => void;
  setWs: (s: WsStatus) => void;
  select: (s: Selection) => void;
}

export const useOps = create<OpsState>((set) => ({
  topology: null, linkHistory: {}, incidents: {}, alerts: [],
  demo: { mode: 'sim', scenario: null, state: 'idle' },
  wsStatus: 'connecting', lastUpdate: 0, selection: null,
  setWs: (wsStatus) => set({ wsStatus }),
  select: (selection) => set({ selection }),
  apply: (m) => set((s) => {
    const lastUpdate = Date.now();
    switch (m.type) {
      case 'snapshot':
        return { topology: m.data.topology, alerts: m.data.alerts, demo: m.data.demo, lastUpdate,
                 incidents: Object.fromEntries(m.data.incidents.map((i) => [i.id, i])) };
      case 'link': {
        if (!s.topology) return {};
        const links = s.topology.links.map((l) => (l.id === m.data.id ? { ...l, ...m.data } : l));
        const pt = { t: m.ts * 1000, util: m.data.utilization, lat: m.data.latencyMs, loss: m.data.packetLoss };
        const hist = [...(s.linkHistory[m.data.id] ?? []), pt].slice(-150);
        return { topology: { ...s.topology, links }, linkHistory: { ...s.linkHistory, [m.data.id]: hist }, lastUpdate };
      }
      case 'node': {
        if (!s.topology) return {};
        const nodes = s.topology.nodes.map((n) => (n.id === m.data.id ? { ...n, ...m.data } : n));
        return { topology: { ...s.topology, nodes }, lastUpdate };
      }
      case 'service': {
        if (!s.topology) return {};
        const services = s.topology.services.map((x) => (x.id === m.data.id ? { ...x, ...m.data } : x));
        return { topology: { ...s.topology, services }, lastUpdate };
      }
      case 'alert':    return { alerts: [m.data, ...s.alerts].slice(0, 200), lastUpdate };
      case 'incident': return { incidents: { ...s.incidents, [m.data.id]: m.data }, lastUpdate };
      case 'demo':     return { demo: m.data, lastUpdate };
    }
  }),
}));
```
**`frontend/src/hooks/useOpsSocket.ts`**
```ts
import { useEffect } from 'react';
import { connectOps } from '@/lib/ws';
import { useOps } from '@/store/useOps';

export function useOpsSocket() {
  useEffect(() => connectOps(useOps.getState().apply, useOps.getState().setWs), []);
}
```
- استدعِ `useOpsSocket()` مرة وحدة في `Shell.tsx`.
- `OperationsPage`: `const topology = useOps((s) => s.topology)` بدل `staticTopology` (اعرض Skeleton لو `null`). احذف `staticTopology.ts` نهاية اليوم (خلّه للاختبارات فقط).
- مؤشر اتصال في TopBar: نقطة خضراء `open` / صفراء `connecting` / حمراء `closed` + «آخر تحديث قبل Xs».
- **LinkInspector**: 3 Sparklines بـRecharts (`<LineChart>` صغير 320×60 لكل من util/latency/loss) من `linkHistory[id]`، مع خط مرجعي أحمر عند 85% للاستخدام (`<ReferenceLine y={85} />`). عند فتح الرابط اجلب أول تاريخ من `GET /api/links/{id}/metrics`.

### 🟨 AI — Baseline ديناميكي
**`backend/app/intelligence/baseline.py`**
```python
import math
from dataclasses import dataclass

@dataclass
class Stat:
    mean: float = 0.0
    var: float = 0.0
    n: int = 0

class Baseline:
    """EWMA لكل (entity, metric). يتجمّد التعلّم أثناء الشذوذ حتى ما «يتعوّد» على العطل."""
    def __init__(self, alpha: float = 0.05, warmup: int = 20):
        self.alpha, self.warmup = alpha, warmup
        self.stats: dict[tuple[str, str], Stat] = {}

    def score(self, entity: str, metric: str, value: float) -> tuple[float, float]:
        """يرجع (baseline_mean, z). z = 0 أثناء الإحماء."""
        s = self.stats.setdefault((entity, metric), Stat(mean=value))
        if s.n < self.warmup:
            return s.mean, 0.0
        std = max(math.sqrt(s.var), 1e-3, 0.05 * abs(s.mean))
        return s.mean, (value - s.mean) / std

    def learn(self, entity: str, metric: str, value: float, anomalous: bool):
        s = self.stats.setdefault((entity, metric), Stat(mean=value))
        if anomalous:
            return
        d = value - s.mean
        s.mean += self.alpha * d
        s.var = (1 - self.alpha) * (s.var + self.alpha * d * d)
        s.n += 1
```
- `backend/tests/test_baseline.py`: (1) 50 قيمة حول 10 ← `z` لقيمة 10.5 < 3. (2) بعدها قيمة 90 ← `z` > 6. (3) بعد 30 قيمة شاذة مع `anomalous=True` المتوسط ما زال ≈ 10.

### 🟥 INFRA — خدمات APP-01 والكولكتر
```bash
# APP-01 (موصول مؤقتًا بـNAT للتثبيت)
sudo apt update && sudo apt install -y bind9 bind9-utils nginx iperf3 stress-ng python3-psutil snmpd
sudo tee /etc/bind/named.conf.local > /dev/null << 'X'
zone "rootiq.lab" { type master; file "/etc/bind/db.rootiq.lab"; };
X
sudo tee /etc/bind/db.rootiq.lab > /dev/null << 'X'
$TTL 60
@   IN SOA ns1.rootiq.lab. admin.rootiq.lab. ( 2026100101 60 60 600 60 )
@   IN NS  ns1.rootiq.lab.
ns1 IN A   10.10.20.10
app IN A   10.10.20.10
X
sudo sed -i 's/^\s*listen-on-v6.*/\tlisten-on { any; };\n\tallow-query { any; };\n\trecursion no;/' /etc/bind/named.conf.options
sudo named-checkconf && sudo named-checkzone rootiq.lab /etc/bind/db.rootiq.lab
sudo systemctl enable --now named
# صفحة الصحة
sudo sed -i 's#location / {#location = /health { default_type text/plain; return 200 "ok"; }\n\tlocation / {#' /etc/nginx/sites-available/default
sudo nginx -t && sudo systemctl reload nginx
sudo systemctl enable --now iperf3 || (iperf3 -s -D)
```
انسخ الملفات النهائية إلى `lab/app01/` في الريبو (`db.rootiq.lab`, `named.conf.local`, `setup.sh` يجمع الأوامر أعلاه) ثم **افصل NAT**.

```bash
# COLLECTOR-01
sudo apt update && sudo apt install -y snmp iperf3 dnsutils python3-venv traceroute
snmpwalk -v2c -c rootiq-ro 10.10.10.1 1.3.6.1.2.1.2.2.1.2      # ifDescr: ثبّت ifIndex لكل منفذ
snmpwalk -v2c -c rootiq-ro 10.10.20.11 1.3.6.1.2.1.2.2.1.2
snmpwalk -v2c -c rootiq-ro 10.10.30.12 1.3.6.1.2.1.2.2.1.2
```
حدّث `ifIndex` في `configs/topology.json` بالنتائج الحقيقية (PR منفصل).

### ✅ معايير قبول اليوم 3
- [ ] `ROOTIQ_MODE=sim` ← الخريطة تتذبذب أرقامها كل ثانية (روابط تتحرك بسرعة مختلفة).
- [ ] حدث يدوي يغيّر الخريطة خلال ≤ 1 ثانية:
```bash
curl -s -X POST localhost:8000/api/events -H 'content-type: application/json' -H 'x-rootiq-token: change-me-ingest' \
 -d '{"sourceId":"r1","sourceType":"router","interface":"Gi0/0","metric":"link_utilization","value":93,"unit":"percent"}'
```
  (في وضع sim أوقف المحاكي مؤقتًا بمتغير `SIM_PAUSED=1` عشان ما يكتب فوقه)
- [ ] نفس الأمر بـ`"sourceId":"zz"` → `422` · وبدون التوكن → `401`.
- [ ] أوقف الباك إند 10 ثواني وشغّله: المؤشر يصير أحمر ثم أخضر، والبيانات ترجع بدون Refresh.
- [ ] Sparklines الرابط تتحرك.
- [ ] `dig @10.10.20.10 app.rootiq.lab +short` من الكولكتر → `10.10.20.10` · `curl -s http://10.10.20.10/health` → `ok` · `iperf3 -c 10.10.20.10 -t 3` ينجح.
- [ ] `pytest -q` كله أخضر.
- [ ] `git tag day-03`

---

# اليوم 4 — الكولكتر الحي + هيكل الواجهة الكامل

**الهدف:** بيانات المختبر الحقيقي تظهر على الخريطة (`ROOTIQ_MODE=live`)، والواجهة تصير شكلها «منتج NOC» مو «صفحة تجريبية».
**المخرجات:** `collector.py` · `app01 agent` · KPI Strip · TopBar · Devices page · Services panel.

### 🟥 INFRA + 🟩 BE — الكولكتر (`lab/collector/collector.py`)
```python
"""RootIQ collector — يشتغل على COLLECTOR-01، يقيس كل 2 ثانية ويدفع دفعة أحداث للباك إند."""
import asyncio, os, re, subprocess, time
from datetime import datetime, timezone
import dns.resolver, httpx

BACKEND = os.environ["ROOTIQ_BACKEND"]                    # http://192.168.100.20:8000
TOKEN = os.environ["ROOTIQ_INGEST_TOKEN"]
COMMUNITY = os.environ.get("SNMP_COMMUNITY", "rootiq-ro")
INTERVAL = 2.0
# (device, mgmt_ip, interface, ifIndex, speed_mbps) — نفس القيم في topology.json
PORTS = [("r1", "10.10.10.1", "Gi0/0", 1, 10), ("r1", "10.10.10.1", "Gi0/1", 2, 1000)]
# لكل رابط: هدف القفزة البعيدة والقريبة لحساب فرق الزمن
HOPS = {"link-r1-sw2": (None, "10.10.30.1"), "link-r1-sw1": ("10.10.30.1", "10.10.20.11"),
        "link-sw1-app01": ("10.10.20.11", "10.10.20.10")}
OID = {"in": "1.3.6.1.2.1.31.1.1.1.6", "out": "1.3.6.1.2.1.31.1.1.1.10",
       "disc": "1.3.6.1.2.1.2.2.1.19", "oper": "1.3.6.1.2.1.2.2.1.8"}
prev: dict = {}

def ev(source_id, source_type, metric, value, unit, interface=None, **meta):
    return {"sourceId": source_id, "sourceType": source_type, "metric": metric, "value": round(value, 3),
            "unit": unit, "interface": interface, "timestamp": datetime.now(timezone.utc).isoformat(), "metadata": meta}

def snmpget(ip: str, oids: list[str]) -> list[int]:
    out = subprocess.run(["snmpget", "-v2c", "-c", COMMUNITY, "-t", "1", "-r", "0", "-Oqv", ip, *oids],
                         capture_output=True, text=True, timeout=3)
    return [int(re.sub(r"\D", "", x) or 0) for x in out.stdout.split()]

def poll_ports():
    events, now = [], time.time()
    for dev, ip, ifname, idx, speed in PORTS:
        try:
            i, o, d, op = snmpget(ip, [f'{OID["in"]}.{idx}', f'{OID["out"]}.{idx}', f'{OID["disc"]}.{idx}', f'{OID["oper"]}.{idx}'])
        except Exception:
            events.append(ev(dev, "router", "poll_timeout", 1, "bool", ifname)); continue
        key = (dev, ifname)
        if key in prev:
            t0, i0, o0, d0 = prev[key]
            dt = max(now - t0, 0.5)
            util = max(i - i0, o - o0) * 8 / (dt * speed * 1e6) * 100
            events += [ev(dev, "router", "link_utilization", min(util, 100), "percent", ifname, collector="snmp"),
                       ev(dev, "router", "if_out_discards_rate", max(d - d0, 0) / dt, "pps", ifname, collector="snmp")]
        events.append(ev(dev, "router", "if_oper_status", 1 if op == 1 else 0, "bool", ifname, collector="snmp"))
        prev[key] = (now, i, o, d)
    return events

def ping(ip: str) -> tuple[float, float]:
    out = subprocess.run(["ping", "-n", "-q", "-c", "5", "-i", "0.2", "-W", "1", ip], capture_output=True, text=True).stdout
    loss = float(re.search(r"([\d.]+)% packet loss", out).group(1))
    m = re.search(r"= [\d.]+/([\d.]+)/", out)
    return (float(m.group(1)) if m else 1000.0), loss

def poll_hops():
    rtt = {}
    for ip in {"10.10.30.1", "10.10.20.11", "10.10.20.10"}:
        rtt[ip] = ping(ip)
    events = []
    for link, (near, far) in HOPS.items():
        lat_far, loss_far = rtt[far]
        lat_near, loss_near = rtt[near] if near else (0.0, 0.0)
        events += [ev(link, "link", "link_latency_ms", max(lat_far - lat_near, 0), "ms", collector="icmp"),
                   ev(link, "link", "link_packet_loss", max(loss_far - loss_near, 0), "percent", collector="icmp")]
    return events

def poll_services():
    events = []
    r = dns.resolver.Resolver(configure=False); r.nameservers = ["10.10.20.10"]; r.lifetime = 1.0
    ok, t0 = 0, time.perf_counter()
    for _ in range(5):
        try: r.resolve("app.rootiq.lab", "A"); ok += 1
        except Exception: pass
    events += [ev("svc-dns", "service", "dns_success_rate", ok * 20, "percent", collector="dns"),
               ev("svc-dns", "service", "dns_latency_ms", (time.perf_counter() - t0) * 1000 / 5, "ms", collector="dns")]
    try:
        ip = r.resolve("app.rootiq.lab", "A")[0].to_text()          # الويب يعتمد على DNS فعلًا
        t0 = time.perf_counter()
        resp = httpx.get(f"http://{ip}/health", headers={"Host": "app.rootiq.lab"}, timeout=2.0)
        events += [ev("svc-web", "service", "http_ok", 1 if resp.status_code == 200 else 0, "bool", collector="http"),
                   ev("svc-web", "service", "http_latency_ms", (time.perf_counter() - t0) * 1000, "ms", collector="http")]
    except Exception:
        events.append(ev("svc-web", "service", "http_ok", 0, "bool", collector="http"))
    try:
        h = httpx.get("http://10.10.20.10:9100/metrics", timeout=1.5).json()
        events += [ev("app01", "server", "cpu_percent", h["cpu"], "percent", collector="agent"),
                   ev("app01", "server", "mem_percent", h["mem"], "percent", collector="agent")]
    except Exception:
        events.append(ev("app01", "server", "poll_timeout", 1, "bool", collector="agent"))
    return events

async def main():
    async with httpx.AsyncClient(timeout=3.0) as client:
        while True:
            t0 = time.time()
            batch = await asyncio.gather(*(asyncio.to_thread(f) for f in (poll_ports, poll_hops, poll_services)))
            events = [e for part in batch for e in part]
            try:
                await client.post(f"{BACKEND}/api/events/batch", json={"events": events}, headers={"x-rootiq-token": TOKEN})
            except Exception as ex:
                print("push failed:", ex)
            await asyncio.sleep(max(0.0, INTERVAL - (time.time() - t0)))

if __name__ == "__main__":
    asyncio.run(main())
```
> ليش نحسب الـLatency كـ«فرق قفزات»؟ لأن الـping لـSW1 وAPP-01 يمر عبر R1 Gi0/0. لما تزدحم الطابور على Gi0/0 يرتفع زمن SW1 وAPP-01 معًا، فالفرق (SW1 − R1) يُنسب **للرابط r1-sw1 بالذات**. هذا اللي يخلي الخريطة تلوّن الرابط الصحيح بالأحمر.
> ملاحظة: `poll_timeout` مقبول في الـpipeline كمقياس (أضفه لجدول العتبات: crit عند 1).

```bash
# COLLECTOR-01
cd ~ && python3 -m venv rq && source rq/bin/activate && pip install httpx dnspython
export ROOTIQ_BACKEND=http://<LAPTOP_IP>:8000 ROOTIQ_INGEST_TOKEN=change-me-ingest
python lab/collector/collector.py
```
**`lab/collector/rootiq-collector.service`**
```ini
[Unit]
Description=RootIQ Collector
After=network-online.target
[Service]
Environment=ROOTIQ_BACKEND=http://192.168.100.20:8000
Environment=ROOTIQ_INGEST_TOKEN=change-me-ingest
ExecStart=/home/rootiq/rq/bin/python /home/rootiq/rootiq/lab/collector/collector.py
Restart=always
RestartSec=2
[Install]
WantedBy=multi-user.target
```
```bash
sudo cp lab/collector/rootiq-collector.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable --now rootiq-collector
journalctl -u rootiq-collector -f
```

**`lab/app01/agent.py`** (APP-01 — مقاييس المضيف على 9100)
```python
import json, psutil
from http.server import BaseHTTPRequestHandler, HTTPServer

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404); self.end_headers(); return
        body = json.dumps({"cpu": psutil.cpu_percent(interval=0.3), "mem": psutil.virtual_memory().percent,
                           "disk": psutil.disk_usage("/").percent}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass

HTTPServer(("0.0.0.0", 9100), H).serve_forever()
```
(وحدة systemd مماثلة باسم `rootiq-agent.service`.)

### 🟦 FE — الواجهة تصير منتج
1. **`components/layout/TopBar.tsx`:** شعار RootIQ + اسم الموقع + `ModeBadge` (`LIVE LAB` أخضر نابض / `SIMULATION` أزرق) + مؤشر WS + «Last update» + زر اللغة (placeholder).
2. **`components/layout/KpiStrip.tsx`** — 6 بطاقات محسوبة من الـstore (selectors مع `useMemo`):
   - Infrastructure Health % = `100 × (عدد العناصر healthy) / (الكل)`
   - Active Incidents = الحوادث غير `resolved`
   - Devices Online = العقد اللي حالتها ≠ `unknown`
   - Services Affected = الخدمات ≠ `healthy`
   - MTTD / MTTR = من آخر حادثة محلولة (يظهر `—` الحين)
3. **`pages/DevicesPage.tsx`:** جدول (الاسم، النوع، IP، الحالة، CPU إن وجد، عدد المنافذ) + البحث.
4. **لوحة الخدمات** أسفل يمين الخريطة: شريحة لكل خدمة (`Internal DNS`, `Web Application`) بلونها + آخر قياس (`dns 100% · 4ms`, `http 42ms`).
5. **DeviceInspector:** قسم «Live metrics» من `node.metrics` (CPU/Mem كـprogress bars).
6. **تفاصيل التصميم (لا تهملها — الحكام يحكمون بعيونهم أول 10 ثواني):** خلفية شبكية داكنة، أرقام `font-mono tabular-nums`، مسافات 8px grid، لا يوجد نص رمادي على رمادي، كل الألوان من `@theme`.

### 🟨 AI — مولّد الشذوذ والتنبيهات الخام
**`backend/app/intelligence/detector.py`**
```python
from dataclasses import dataclass
from .baseline import Baseline
from .thresholds import static_severity

@dataclass
class Anomaly:
    entity_id: str
    metric: str
    value: float
    baseline: float
    severity: float          # 0..1
    first_seen: float
    last_seen: float

class Detector:
    def __init__(self):
        self.baseline = Baseline()
        self.active: dict[tuple[str, str], Anomaly] = {}
        self.alert_level: dict[tuple[str, str], float] = {}

    def observe(self, entity: str, metric: str, value: float, ts: float):
        """يرجع (anomaly|None, raw_alert_level|None). raw alert = عبور عتبة جديد (مثل NMS تقليدي)."""
        base, z = self.baseline.score(entity, metric, value)
        sev_static = static_severity(metric, value)
        sev_z = min(1.0, max(0.0, (abs(z) - 3) / 3)) if metric not in ("http_ok", "if_oper_status") else 0.0
        sev = max(sev_static, sev_z)
        key = (entity, metric)
        anomaly = None
        if sev >= 0.5:
            a = self.active.get(key)
            if a is None:
                a = self.active[key] = Anomaly(entity, metric, value, base, sev, ts, ts)
            a.value, a.severity, a.last_seen = value, max(a.severity, sev), ts
            anomaly = a
        elif key in self.active and ts - self.active[key].last_seen > 10:
            del self.active[key]                                   # تعافى 10 ثواني متواصلة
        self.baseline.learn(entity, metric, value, anomalous=sev >= 0.5)
        level = 1.0 if sev_static >= 1 else 0.5 if sev_static >= 0.5 else 0.0
        prev = self.alert_level.get(key, 0.0)
        self.alert_level[key] = level
        raw_alert = level if level > prev else None                # تنبيه عند الارتفاع فقط
        return anomaly, raw_alert
```
- `tests/test_detector.py`: تسلسل 30 قيمة طبيعية ثم 97 ← أول `raw_alert == 1.0` وAnomaly واحد؛ تكرار 97 عشر مرات ← **لا** تنبيهات إضافية؛ رجوع للطبيعي 15 ثانية ← `active` فاضي.

### ✅ معايير قبول اليوم 4
- [ ] `ROOTIQ_MODE=live` + الكولكتر شغّال ← الخريطة تعرض أرقام المختبر (استخدام r1-sw1 ≈ منخفض، latency بالملي ثانية).
- [ ] شغّل من الكولكتر `iperf3 -c 10.10.20.10 -u -b 15M -t 20` ← خلال ≤ 4 ثواني يصير `link-r1-sw1` أصفر/أحمر على الشاشة ويرتفع الاستخدام > 85%.
- [ ] `journalctl -u rootiq-collector` بدون أخطاء push لـ5 دقائق.
- [ ] `curl -s http://10.10.20.10:9100/metrics` من الكولكتر يرجع JSON.
- [ ] KPI Strip يعرض 6 بطاقات بأرقام منطقية؛ صفحة Devices فيها 5 صفوف.
- [ ] `pytest -q tests/test_detector.py` أخضر.
- [ ] `git tag day-04`

---

# اليوم 5 — حقن الأعطال (Fault Injection) · 🎯 المعلَم M1

**الهدف:** زر واحد في الواجهة يحقن عطلًا حقيقيًا في المختبر (أو المحاكاة)، والتنبيهات الخام تبدأ تتدفق مثل أي أداة مراقبة تقليدية.
**المخرجات:** `lab_agent.py` بأوامر مسموحة فقط · `/api/demo/*` · DemoControls + Hotkeys · Raw Alerts Feed.

### 🟥 INFRA — Lab Agent (`lab/agent/lab_agent.py` على COLLECTOR-01، منفذ 9000)
```python
"""كل الأوامر هنا Whitelist ثابتة. لا يوجد أي endpoint يقبل أمر نصي من الخارج (ضابط أمان من الوثيقة)."""
import os, subprocess
from fastapi import FastAPI, Header, HTTPException
from netmiko import ConnectHandler

TOKEN = os.environ["LAB_AGENT_TOKEN"]
APP = "rootiq@10.10.20.10"
R1 = dict(device_type="cisco_ios", host="10.10.10.1", username="rootiq", password=os.environ["R1_PASSWORD"])
app = FastAPI(title="RootIQ Lab Agent")
procs: dict[str, subprocess.Popen] = {}

def ssh_app(cmd: str) -> str:
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=3", APP, cmd],
                       capture_output=True, text=True, timeout=15)
    if r.returncode not in (0, 1):
        raise RuntimeError(r.stderr.strip())
    return r.stdout

def r1_config(lines: list[str]) -> str:
    with ConnectHandler(**R1) as c:
        return c.send_config_set(lines)

def start_iperf():
    stop_iperf()
    procs["iperf"] = subprocess.Popen(["iperf3", "-c", "10.10.20.10", "-u", "-b", "15M", "-t", "900"],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_iperf():
    p = procs.pop("iperf", None)
    if p and p.poll() is None:
        p.terminate()

INJECT = {
    "uplink-congestion": start_iperf,
    "dns-failure": lambda: ssh_app("sudo /usr/bin/systemctl stop named"),
    "server-spike": lambda: ssh_app("nohup stress-ng --cpu 2 --cpu-load 100 --timeout 900s >/dev/null 2>&1 &"),
}
REMEDIATE = {
    "uplink-congestion": lambda: r1_config(["interface GigabitEthernet0/0",
                                            "no service-policy output UPLINK-SHAPE",
                                            "service-policy output UPLINK-QOS"]),
    "dns-failure": lambda: ssh_app("sudo /usr/bin/systemctl start named"),
    "server-spike": lambda: ssh_app("pkill -f stress-ng || true"),
}

def auth(token: str | None):
    if token != TOKEN:
        raise HTTPException(401)

@app.post("/inject/{scenario}")
def inject(scenario: str, x_agent_token: str | None = Header(None)):
    auth(x_agent_token)
    if scenario not in INJECT: raise HTTPException(404)
    INJECT[scenario](); return {"ok": True, "scenario": scenario}

@app.post("/remediate/{scenario}")
def remediate(scenario: str, x_agent_token: str | None = Header(None)):
    auth(x_agent_token)
    if scenario not in REMEDIATE: raise HTTPException(404)
    out = REMEDIATE[scenario](); return {"ok": True, "output": str(out)[-500:]}

@app.post("/reset")
def reset(x_agent_token: str | None = Header(None)):
    auth(x_agent_token)
    stop_iperf()
    r1_config(["interface GigabitEthernet0/0", "no service-policy output UPLINK-QOS", "service-policy output UPLINK-SHAPE"])
    ssh_app("sudo /usr/bin/systemctl start named"); ssh_app("pkill -f stress-ng || true")
    return {"ok": True}

@app.get("/health")
def health():
    return {"ok": True, "iperfRunning": bool(procs.get("iperf") and procs["iperf"].poll() is None)}
```
```bash
# COLLECTOR-01
source ~/rq/bin/activate && pip install fastapi uvicorn netmiko
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519 && ssh-copy-id rootiq@10.10.20.10
# APP-01: صلاحيات محدودة جدًا
echo 'rootiq ALL=(root) NOPASSWD: /usr/bin/systemctl stop named, /usr/bin/systemctl start named' | sudo tee /etc/sudoers.d/rootiq
sudo visudo -cf /etc/sudoers.d/rootiq
# تشغيل الوكيل
LAB_AGENT_TOKEN=change-me-agent R1_PASSWORD='RootIQ-Lab-2026' uvicorn lab_agent:app --host 0.0.0.0 --port 9000 --app-dir lab/agent
```
- اكتب أيضًا `lab/scenarios/{uplink_congestion,dns_failure,server_spike,reset}.sh` كنسخ يدوية بـ`curl` للوكيل (خطة احتياطية لو الباك إند خرب).

### 🟩 BE — مسارات الديمو
**`backend/app/services/lab_client.py`**
```python
import httpx
from app.core.config import settings

async def call(path: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post(f"{settings.lab_agent_url}{path}", headers={"x-agent-token": settings.lab_agent_token})
        r.raise_for_status()
        return r.json()
```
**`backend/app/api/demo.py`**
```python
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Request
from app.services import lab_client
from app.services.hub import hub

router = APIRouter(prefix="/demo", tags=["demo"])
SCENARIOS = {"uplink-congestion", "dns-failure", "server-spike"}

@router.post("/inject/{scenario}")
async def inject(scenario: str, request: Request):
    st = request.app.state
    if scenario not in SCENARIOS: raise HTTPException(404, "unknown scenario")
    if st.demo["state"] != "idle": raise HTTPException(409, "reset first")
    if st.demo["mode"] == "sim": st.simulator.inject(scenario)
    else: await lab_client.call(f"/inject/{scenario}")
    st.demo.update(scenario=scenario, state="injected", injectedAt=datetime.now(timezone.utc).isoformat())
    await hub.broadcast("demo", st.demo)
    return st.demo

@router.post("/reset")
async def reset(request: Request):
    st = request.app.state
    if st.demo["mode"] == "sim": st.simulator.reset()
    else: await lab_client.call("/reset")
    await st.incidents.archive_all()          # يوم 6: يغلق أي حادثة مفتوحة كـ«reset»
    st.detector.active.clear(); st.detector.alert_level.clear()   # تصفير الشذوذ النشط مع إبقاء الـbaseline
    st.demo.update(scenario=None, state="idle", injectedAt=None)
    await hub.broadcast("demo", st.demo)
    return st.demo
```
- `app.state.demo = {"mode": settings.rootiq_mode, "scenario": None, "state": "idle", "injectedAt": None}`.
- وسّع `Pipeline.ingest` بعد `state.update`:
```python
        anomaly, raw_level = self.detector.observe(ev.source_id, ev.metric, ev.value, ev.timestamp.timestamp())
        if raw_level:
            alert = {"id": f"alr-{next(self._seq):05d}", "sourceId": ev.source_id, "metric": ev.metric,
                     "value": ev.value, "severity": "critical" if raw_level >= 1 else "warning",
                     "ts": ev.timestamp.isoformat()}
            self.alerts.appendleft(alert)                  # deque(maxlen=200)
            await hub.broadcast("alert", alert)
        if anomaly:
            await self.incidents.on_anomaly(anomaly)       # يوم 6 (الحين no-op)
```
> **مهم للقصة:** التنبيهات الخام هي «ما تشوفه الأدوات التقليدية». نعدّها ونعرضها عمدًا لأن الفرق بين عددها وعدد الحوادث = قيمة RootIQ.

### 🟦 FE — لوحة التحكم بالديمو
**`frontend/src/lib/api.ts`**
```ts
import type { Incident, Topology } from './types';

async function j<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const res = await fetch(input, { headers: { 'content-type': 'application/json' }, ...init });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json() as Promise<T>;
}
export type Scenario = 'uplink-congestion' | 'dns-failure' | 'server-spike';

export const api = {
  topology: () => j<Topology>('/api/topology'),
  saveLayout: (positions: Record<string, { x: number; y: number }>) =>
    j('/api/topology/layout', { method: 'PUT', body: JSON.stringify({ positions }) }),
  linkMetrics: (id: string) => j<Record<string, [number, number][]>>(`/api/links/${id}/metrics?minutes=5`),
  incidents: () => j<Incident[]>('/api/incidents'),
  inject: (s: Scenario) => j(`/api/demo/inject/${s}`, { method: 'POST' }),
  reset: () => j('/api/demo/reset', { method: 'POST' }),
  setMode: (mode: 'live' | 'sim') => j('/api/demo/mode', { method: 'POST', body: JSON.stringify({ mode }) }),
  approve: (actionId: string, decidedBy: string) =>
    j(`/api/actions/${actionId}/approve`, { method: 'POST', body: JSON.stringify({ decidedBy }) }),
  reject: (actionId: string, decidedBy: string, reason: string) =>
    j(`/api/actions/${actionId}/reject`, { method: 'POST', body: JSON.stringify({ decidedBy, reason }) }),
};
```
**`frontend/src/hooks/useHotkeys.ts`** (اختصارات المقدّم — لا يحتاج يدور على الزر وسط العرض)
```ts
import { useEffect } from 'react';
import { api } from '@/lib/api';

export function useHotkeys(onTogglePresenter: () => void) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (!e.shiftKey || (e.target as HTMLElement).closest('input,textarea')) return;
      const map: Record<string, () => unknown> = {
        Digit1: () => api.inject('uplink-congestion'),
        Digit2: () => api.inject('dns-failure'),
        Digit3: () => api.inject('server-spike'),
        KeyR: () => api.reset(),
        KeyP: onTogglePresenter,
      };
      if (map[e.code]) { e.preventDefault(); Promise.resolve(map[e.code]()).catch(console.error); }
    };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [onTogglePresenter]);
}
```
- **`components/demo/DemoControls.tsx`:** لوحة عائمة أسفل يسار: 3 أزرار (`Inject Uplink Congestion` / `Inject DNS Failure` / `Inject Server Spike`) + `Reset Demo` + حالة `idle/injected/...` + Toast للأخطاء. الأزرار disabled إذا `demo.state !== 'idle'`. تحت كل زر اختصاره (`⇧1`).
- **عمود «Raw alerts»:** قائمة يسار الخريطة (عرض 260px) تعرض `alerts` بأنيميشن دخول (`motion.li` مع `initial={{opacity:0,x:-12}}`) + عدّاد كبير أعلاها. العنوان: *What a traditional NMS shows you*.

### 🟨 AI — ربط الكاشف بالـpipeline + اختبار تكامل
- `tests/test_pipeline_sim.py`: شغّل `Simulator` بدون `sleep` (استدعِ دالة `step()` مستخرجة من `run()`) 60 خطوة طبيعية ثم `inject("uplink-congestion")` 20 خطوة ← تأكد إن أول تنبيه خام على `link-r1-sw1|link_utilization` وإن عدد التنبيهات بين 5 و15.
- أعد هيكلة `Simulator.run` إلى `async def step(self)` + حلقة، عشان الاختبارات ما تنتظر.

### ✅ معايير قبول اليوم 5 — 🎯 M1
- [ ] **sim:** `Shift+1` ← خلال ≤ 3 ثواني `link-r1-sw1` أحمر، الحركة على الرابط تسرع، والتنبيهات الخام تبدأ تنزل.
- [ ] **live:** `curl -s -X POST localhost:8000/api/demo/inject/uplink-congestion` ← نفس النتيجة من المختبر الحقيقي خلال ≤ 6 ثواني.
- [ ] حقن ثاني بدون Reset ← `409`.
- [ ] `Shift+R` ← المختبر يرجع طبيعي (`ssh collector 'pgrep iperf3'` ما يرجع شيء، و`show policy-map interface Gi0/0` يرجع `UPLINK-SHAPE`) والخريطة خضراء خلال ≤ 20 ثانية.
- [ ] DNS: `Shift+2` ← `dig @10.10.20.10 app.rootiq.lab` يفشل و`svc-dns` أحمر. CPU: `Shift+3` ← `app01` CPU > 90%.
- [ ] `curl -s -X POST http://<collector>:9000/inject/rm-rf` ← `401` أو `404` (لا يوجد تنفيذ أوامر حرة).
- [ ] سجّل فيديو 60 ثانية للمعلم M1 في `docs/progress/m1.mp4`.
- [ ] `git tag day-05 m1`

---

# اليوم 6 — الحوادث (Correlation + Lifecycle + Persistence)

**الهدف:** عطل واحد = **حادثة واحدة** تجمع كل الأعراض المرتبطة، محفوظة في PostgreSQL، وتظهر في لوحة الحادثة والقائمة والـTimeline.

### 🟩 BE — قاعدة البيانات
**`backend/app/db/session.py`**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): ...
```
**`backend/app/db/models.py`** (الكيانات من القسم 10 في الوثيقة + `runs` و`audit_log`)
```python
from datetime import datetime
from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .session import Base

class IncidentRow(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String(16), primary_key=True)          # INC-0001
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(32), index=True)
    severity: Mapped[str] = mapped_column(String(16))
    root_cause: Mapped[str | None] = mapped_column(String(64))
    confidence: Mapped[float | None] = mapped_column(Float)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    snapshot: Mapped[dict] = mapped_column(JSON)                            # كائن Incident كامل كما يُرسل للواجهة

class EvidenceRow(Base):
    __tablename__ = "incident_evidence"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    entity_id: Mapped[str] = mapped_column(String(64))
    metric: Mapped[str] = mapped_column(String(64))
    value: Mapped[float] = mapped_column(Float)
    baseline: Mapped[float] = mapped_column(Float)
    relation_type: Mapped[str] = mapped_column(String(16))                  # cause | symptom
    weight: Mapped[float] = mapped_column(Float, default=0)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class ActionRow(Base):
    __tablename__ = "actions"
    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    action_type: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON)
    approval_status: Mapped[str] = mapped_column(String(16))
    decided_by: Mapped[str | None] = mapped_column(String(64))
    reason: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

class AuditRow(Base):
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    actor: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(String(64))
    target: Mapped[str] = mapped_column(String(64))
    detail: Mapped[dict] = mapped_column(JSON)

class RunRow(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scenario: Mapped[str] = mapped_column(String(32))
    mode: Mapped[str] = mapped_column(String(8))
    incident_id: Mapped[str | None] = mapped_column(String(16))
    metrics: Mapped[dict] = mapped_column(JSON)       # mttd, ttr, mttr, rawAlerts, incidents, correct
```
- في `lifespan`: `Base.metadata.create_all(engine)` (لا نحتاج Alembic في الهاكاثون).

### 🟨 AI — التجميع (`backend/app/intelligence/correlate.py`)
```python
from .graph import TopologyGraph

WINDOW_S = 120

class Correlator:
    def __init__(self, graph: TopologyGraph):
        self.g = graph

    def related(self, a: str, b: str) -> bool:
        if a == b:
            return True
        if a in self.g.downstream(b) or b in self.g.downstream(a):
            return True
        if set(self.g.services_through(a)) & set(self.g.services_through(b)):
            return True
        try:
            return self.g.hop_distance(a, b) <= 3
        except Exception:
            return False

    def pick(self, entity: str, ts: float, open_incidents: list) -> object | None:
        """يرجع الحادثة المفتوحة المناسبة أو None (= افتح حادثة جديدة)."""
        best = None
        for inc in open_incidents:
            if ts - inc.last_activity > WINDOW_S:
                continue
            if any(self.related(entity, m) for m in inc.members):
                if best is None or inc.last_activity > best.last_activity:
                    best = inc
        return best
```
- `tests/test_correlate.py`: أعراض السيناريو 1 (`link-r1-sw1`, `svc-web`, `svc-dns`) ← كلها `related`. عرض على `link-sw2-collector01` فقط بعد 200 ثانية ← حادثة جديدة.

### 🟩 BE — `services/incident_service.py` (الملامح)
- يحتفظ بالحوادث المفتوحة في الذاكرة (`dict[id, IncidentState]`) + يكتب `snapshot` في `incidents` بعد كل تغيير.
- `on_anomaly(a)`: `inc = correlator.pick(...)` ← لو `None` افتح `INC-000N` بحالة `open` و`timings.firstAnomalyAt/detectedAt` و`injectedAt` من `app.state.demo`؛ أضف `a.entity_id` لـ`members`، خزّن Evidence، حدّث `rawAlertCount`، انقل الحالة لـ`investigating`، اعمل `broadcast("incident", ...)`.
- `archive_all()`: أي حادثة مفتوحة ← `resolved` بملاحظة `reset`.
- `GET /api/incidents` (آخر 50) و`GET /api/incidents/{id}`.
- العنوان المؤقت: `"Correlated incident · {n} symptoms"` (يتغير بعد RCA).

### 🟦 FE — لوحة الحادثة v1 + القائمة + الـTimeline
1. **`components/incidents/IncidentPanel.tsx`** (عمود يمين 420px، يظهر تلقائيًا عند أول حادثة مفتوحة مع `AnimatePresence`):
   - Header: `INC-0001` · Severity chip · عنوان · مدة مفتوحة حيّة (`mm:ss`).
   - **Status stepper** أفقي بمراحل دورة الحياة (2.6) — المرحلة الحالية مضيئة.
   - «Correlated symptoms (n)»: قائمة الأعراض مع أيقونة النوع والقيمة الحالية.
   - Placeholder لقسم «Root cause» (يوم 7) و«Recommended action» (يوم 8).
2. **تلوين الخريطة:** احسب `focus` في `OperationsPage` بـ`useMemo` من الحادثة النشطة — قبل الـRCA كل الأعضاء `impact` (برتقالي).
3. **`pages/IncidentsPage.tsx`:** جدول (ID، العنوان، الحالة، الخطورة، الفتح، المدة، السبب الجذري، الثقة) + فلتر حالة + الضغط يفتح `/incidents/:id` ويعيد استخدام `IncidentPanel`.
4. **`components/timeline/Timeline.tsx`** (شريط سفلي 180px): محور زمني أفقي آخر 5 دقائق؛ نقاط التنبيهات الخام (أصفر/أحمر) + علامات المراحل (Injected ▲، Incident opened ●). مرور الماوس على نقطة ← `select({kind, id: sourceId})` وتمييز العنصر في الخريطة.

### 🟥 INFRA — Syslog كدليل إضافي
- في الكولكتر: مستمع UDP 514 (`asyncio.DatagramProtocol`) يحلل `%LINK-3-UPDOWN` و`%LINEPROTO-5-UPDOWN` و`%QOS` ويرسلها كأحداث `metric="syslog_link_down"` بقيمة 1 على الرابط المطابق. (تحتاج `sudo setcap 'cap_net_bind_service=+ep' ~/rq/bin/python3.12` أو تشغيله بـroot.)
- اختبار: `interface Gi0/1` ← `shutdown` ثم `no shutdown` على SW2 ويظهر حدث.

### ✅ معايير قبول اليوم 6
- [ ] sim: `Shift+1` ← **حادثة واحدة فقط** في `GET /api/incidents` تحتوي ≥ 3 أعراض (`link-r1-sw1`, `svc-web`, `svc-dns`).
```bash
curl -s localhost:8000/api/incidents | python3 -c "import sys,json;d=json.load(sys.stdin);print(len([i for i in d if i['status']!='resolved']), d[0]['rawAlertCount'])"
# المتوقع: 1 و ≥ 5
```
- [ ] نفس الشي في live.
- [ ] أعد تشغيل الباك إند ← `GET /api/incidents` ما زال فيه الحادثة (Persistence).
- [ ] الواجهة: اللوحة تنزلق من اليمين، الـstepper على `investigating`، والأعضاء برتقالية في الخريطة.
- [ ] `pytest -q` أخضر (بما فيه `test_correlate.py`).
- [ ] `git tag day-06`

---

# اليوم 7 — تحليل السبب الجذري (RCA) · 🎯 المعلَم M2

**الهدف:** خلال < 60 ثانية من الحقن: الحادثة تسمّي **السبب الصحيح** بثقة وأدلة مقاسة، وأعلى 3 مرشحين مع تفكيك الدرجة، والخريطة تلوّن السبب بالأحمر والمسار المتأثر بالبرتقالي.

### 🟨 AI — `backend/app/intelligence/rca.py`
```python
from dataclasses import dataclass, field
from math import exp
from .graph import TopologyGraph

WEIGHTS = {"metric_anomaly": 0.30, "dependency_overlap": 0.25, "temporal_proximity": 0.20,
           "blast_radius": 0.15, "historical_support": 0.10}      # نفس صيغة الوثيقة
SUPPRESSION = 0.5          # عرَض خلف مرشح شاذ ← نصف الدرجة
LOW_CONFIDENCE = 0.55      # تحتها نقول بصراحة: يحتاج تحقيق إضافي

@dataclass
class Candidate:
    entity_id: str
    label: str
    score: float
    components: dict[str, float]
    evidence: list[str] = field(default_factory=list)
    suppressed_by: str | None = None

def fmt(a) -> str:
    unit = {"link_utilization": "%", "link_packet_loss": "%", "dns_success_rate": "%", "cpu_percent": "%",
            "mem_percent": "%"}.get(a.metric, " ms" if a.metric.endswith("_ms") else "")
    return f"{a.metric} = {a.value:.1f}{unit} (baseline {a.baseline:.1f}{unit})"

def rank(anomalies: list, affected_services: list[str], g: TopologyGraph, history) -> tuple[list[Candidate], float]:
    by_entity: dict[str, list] = {}
    for a in anomalies:
        by_entity.setdefault(a.entity_id, []).append(a)
    if not by_entity:
        return [], 0.0
    t0 = min(a.first_seen for a in anomalies)
    anomalous = set(by_entity)
    paths = [set(g.service_dependencies(s)) for s in affected_services]
    out: list[Candidate] = []
    for c, own in by_entity.items():                      # فقط العناصر اللي فعلًا شاذة ممكن تكون سبب
        first = min(a.first_seen for a in own)
        comps = {
            "metric_anomaly": max(a.severity for a in own),
            "dependency_overlap": (sum(1 for p in paths if c in p) / len(paths)) if paths else 0.0,
            "temporal_proximity": exp(-(first - t0) / 30.0),
            "blast_radius": len(anomalous & g.downstream(c)) / max(1, len(anomalous - {c})),
            "historical_support": history.support(c),
        }
        score = sum(WEIGHTS[k] * v for k, v in comps.items())
        upstream_bad = sorted(anomalous & g.upstream(c))
        suppressed_by = upstream_bad[0] if upstream_bad else None
        if suppressed_by:
            score *= SUPPRESSION
        ev = [fmt(a) + f" at +{a.first_seen - t0:.0f}s" for a in sorted(own, key=lambda x: -x.severity)]
        if comps["dependency_overlap"] > 0:
            ev.append(f"{sum(1 for p in paths if c in p)}/{len(paths)} affected services depend on this element")
        if comps["historical_support"] > 0:
            ev.append(f"Matches {history.count(c)} previously resolved incident(s)")
        out.append(Candidate(c, g.label(c), round(score, 3), {k: round(v, 3) for k, v in comps.items()}, ev, suppressed_by))
    out.sort(key=lambda x: x.score, reverse=True)
    top = out[:3]
    s1 = top[0].score
    s2 = top[1].score if len(top) > 1 else 0.0
    confidence = max(0.0, min(0.99, s1 - max(0.0, 0.15 - (s1 - s2))))   # منافس قريب ← نخفض الثقة
    return top, round(confidence, 2)
```
**`backend/app/intelligence/history.py`**
```python
import json
from pathlib import Path

class History:
    """يتعلم من الحوادث المحلولة: كل مرة يُعتمد سبب ويتعافى النظام نزيد رصيده."""
    def __init__(self, path: str = "data/history.json"):
        self.path = Path(path)
        self.counts: dict[str, int] = json.loads(self.path.read_text()) if self.path.exists() else {}

    def count(self, entity: str) -> int:
        return self.counts.get(entity, 0)

    def support(self, entity: str) -> float:
        n = self.count(entity)
        return n / (n + 1)                      # 0 → 0.5 → 0.67 → 0.75 ...

    def record(self, entity: str):
        self.counts[entity] = self.count(entity) + 1
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.counts, indent=2))
```
> **لماذا هذا الترتيب يطلع صح؟** في الازدحام: `svc-dns` و`svc-web` شاذين، لكن `link-r1-sw1` يقع **قبلهم** في مسار الاعتماد وهو شاذ ← يتم إخمادهم (×0.5) ويطلع الرابط أولًا بدرجة ≈ 0.90. في فشل DNS: الرابط سليم (ما هو شاذ أصلًا) ← `svc-dns` الأول، و`svc-web` مُخمد لأنه يعتمد على DNS. في ضغط CPU: `app01` أول لأن `svc-web/svc-dns` خلفه.

**`backend/tests/test_rca.py`** — 3 اختبارات حاسمة (واحد لكل سيناريو) + اختبار «عدم يقين»:
```python
from app.intelligence.detector import Anomaly
from app.intelligence.rca import rank
from tests.test_graph import g

class NoHistory:
    def support(self, e): return 0.0
    def count(self, e): return 0

A = lambda e, m, v, b, s, t: Anomaly(e, m, v, b, s, t, t)

def test_congestion_ranks_uplink_first():
    an = [A("link-r1-sw1", "link_utilization", 97, 14, 1.0, 100), A("link-r1-sw1", "link_latency_ms", 86, 2.5, 1.0, 102),
          A("svc-web", "http_latency_ms", 1450, 42, 1.0, 106), A("svc-dns", "dns_success_rate", 72, 100, 0.5, 108)]
    top, conf = rank(an, ["svc-web", "svc-dns"], g, NoHistory())
    assert top[0].entity_id == "link-r1-sw1" and conf >= 0.8
    assert top[1].suppressed_by == "link-r1-sw1"

def test_dns_failure_ranks_dns_first():
    an = [A("svc-dns", "dns_success_rate", 0, 100, 1.0, 100), A("svc-web", "http_ok", 0, 1, 1.0, 102)]
    top, _ = rank(an, ["svc-web", "svc-dns"], g, NoHistory())
    assert top[0].entity_id == "svc-dns"

def test_cpu_spike_ranks_server_first():
    an = [A("app01", "cpu_percent", 98, 18, 1.0, 100), A("svc-web", "http_latency_ms", 1100, 42, 1.0, 104)]
    top, _ = rank(an, ["svc-web"], g, NoHistory())
    assert top[0].entity_id == "app01"

def test_isolated_anomaly_without_service_impact_is_low_confidence():
    # رابط شاذ لحاله بدون أي خدمة متأثرة ← لا نخترع يقين: needsInvestigation
    an = [A("link-r1-sw2", "link_utilization", 90, 6, 1.0, 100)]
    _, conf = rank(an, [], g, NoHistory())
    assert conf < 0.55
```

### 🟩 BE — التحليل التلقائي + المسجّل
- في `incident_service`: بعد كل عضو جديد جدول تحليل بعد **3 ثواني هدوء** (debounce)، وبحد أقصى **10 ثواني** من فتح الحادثة (حتى ما يتأخر أبدًا عن هدف 60 ثانية).
- `analyze(inc)`: `affected = [s for s in services if s in inc.members]` ← `rank(...)` ← عبّئ `rootCause`, `candidates`, `confidence`, `needsInvestigation = conf < 0.55`, `causePath = [root]`، `impactPath = sorted(g.downstream(root) ∩ topology elements)`، العنوان: `"Uplink congestion on R1 Gi0/0"` / `"DNS service failure on APP-01"` / `"Resource pressure on APP-01"` حسب نوع السبب والمقياس الأعلى، `timings.analyzedAt`، الحالة ← `recommendation_ready`.
- `POST /api/incidents/{id}/analyze` يعيد التحليل يدويًا (مطلوب في الوثيقة).
- **المسجّل** `services/recorder.py`: لو `RECORD_EVENTS=1` كل حدث (بعد ترجمة المنفذ إلى رابط) يُكتب سطر JSON في `data/recordings/<YYYYMMDD-HHMM>.jsonl` بالصيغة `{"ts": <epoch float>, "sourceId": ..., "sourceType": ..., "metric": ..., "value": ..., "unit": ...}` — نفس الصيغة يقرأها `replay.py` و`anomaly.py`.
- **أداة إعادة التشغيل** `backend/app/tools/replay.py`:
```bash
python -m app.tools.replay data/recordings/20261007-1030-congestion.jsonl --speed 1 --token change-me-ingest
```
  تقرأ الأسطر وترسلها إلى `/api/events/batch` بنفس الفواصل الزمنية (مقسومة على `--speed`). **هذا يصير خطة احتياطية ثالثة**: بيانات حقيقية مسجلة من المختبر تُعاد وقت العرض لو المختبر مات.

### 🟥 INFRA — تسجيل مجموعات البيانات
```bash
# على اللابتوب: RECORD_EVENTS=1 ROOTIQ_MODE=live ثم:
# 1) 15 دقيقة طبيعي بالكامل (لا تلمس شي) → healthy-15m.jsonl
# 2) لكل سيناريو × 3 مرات:
curl -s -X POST localhost:8000/api/demo/inject/uplink-congestion; sleep 90
curl -s -X POST "http://<collector>:9000/remediate/uplink-congestion" -H 'x-agent-token: change-me-agent'; sleep 60
curl -s -X POST localhost:8000/api/demo/reset; sleep 60
```
- سمّ الملفات `data/recordings/<date>-<scenario>-runN.jsonl`، وانسخ نسخة مقصوصة (٣ دقائق) لكل سيناريو إلى `backend/tests/fixtures/`.
- دوّن في `docs/RESULTS.md` لكل تشغيل: وقت ظهور أول شذوذ بعد الحقن، أقصى استخدام، أقصى latency.

### 🟦 FE — شرح السبب بصريًا
1. **`ConfidenceRing.tsx`** (SVG دائرة 96px):
```tsx
export function ConfidenceRing({ value }: { value: number }) {
  const r = 40, c = 2 * Math.PI * r, pct = Math.round(value * 100);
  const color = value >= 0.8 ? '#22c55e' : value >= 0.55 ? '#eab308' : '#f97316';
  return (
    <svg width="96" height="96" viewBox="0 0 96 96" role="img" aria-label={`confidence ${pct}%`}>
      <circle cx="48" cy="48" r={r} stroke="#1f2a4d" strokeWidth="8" fill="none" />
      <circle cx="48" cy="48" r={r} stroke={color} strokeWidth="8" fill="none" strokeLinecap="round"
        strokeDasharray={c} strokeDashoffset={c * (1 - value)} transform="rotate(-90 48 48)"
        style={{ transition: 'stroke-dashoffset 900ms ease' }} />
      <text x="48" y="54" textAnchor="middle" className="fill-slate-100 font-mono text-xl font-bold">{pct}%</text>
    </svg>
  );
}
```
2. **`CandidateRanking.tsx`:** لكل مرشح (حتى 3): الاسم + الدرجة + **شريط مكدّس** من 5 ألوان = `WEIGHTS[k] × components[k]` (Legend صغير تحته) + لو `suppressedBy`: سطر رمادي «Symptom — downstream of R1 Gi0/0 → SW1 Gi0/1».
3. **`EvidenceList.tsx`:** كل دليل: أيقونة المقياس + النص + `+2s` (الزمن النسبي من أول شذوذ) + مقارنة `value vs baseline` بشريط صغير.
4. **`AffectedServices.tsx`:** chips الخدمات المتأثرة بلونها.
5. **حالة `needsInvestigation`:** بانر أصفر: «Low confidence — more investigation required» وما نعرض زر الموافقة كإجراء أساسي (صدق = ثقة الحكام).
6. **الخريطة:** `focus[root] = 'cause'`، و`impactPath` = `'impact'`. عند وصول الـRCA أول مرة: `useReactFlow().fitView({ nodes: [{ id: rootDeviceId }], duration: 800, padding: 0.6 })` ثم ارجع للعرض الكامل بعد 3 ثواني.

### ✅ معايير قبول اليوم 7 — 🎯 M2
- [ ] `pytest -q tests/test_rca.py` → 4 passed.
- [ ] sim ×3: كل مرة `rootCause.entityId == "link-r1-sw1"` و`confidence ≥ 0.8` و`analyzedAt - injectedAt < 20s`.
```bash
curl -s localhost:8000/api/incidents | python3 -c "
import sys,json;from datetime import datetime as D
i=json.load(sys.stdin)[0];t=i['timings']
print(i['rootCause'], (D.fromisoformat(t['analyzedAt'])-D.fromisoformat(t['injectedAt'])).total_seconds())"
```
- [ ] live ×3: نفس الشي و`analyzedAt - injectedAt < 60s` (هدف الوثيقة).
- [ ] الواجهة: الرابط R1 Gi0/0 → SW1 Gi0/1 أحمر نابض، SW1/APP-01/الخدمات برتقالي، الحلقة تعرض الثقة، الأدلة ≥ 2 بأرقام مقاسة.
- [ ] ملفات التسجيل موجودة: `ls data/recordings | wc -l` ≥ 10.
- [ ] `git tag day-07 m2`

---

# اليوم 8 — الإجراء والموافقة والتعافي · 🎯 المعلَم M3

**الهدف:** الحلقة الكاملة للسيناريو الأول: توصية آمنة ← **Reject** (ما يتغير شي ويتسجل السبب) ← **Approve** ← يُطبّق QoS فعليًا على R1 ← المؤشرات ترجع طبيعية ← الحادثة `resolved` بالأوقات.

### 🟩 BE — `services/action_service.py`
```python
RECOMMENDATIONS = {
    "link": {"actionType": "apply_qos_policy", "risk": "low", "scenario": "uplink-congestion",
             "description": "Apply UPLINK-QOS on R1 Gi0/0: police bulk traffic (port 5201) to 2 Mbps and fair-queue critical flows.",
             "alternatives": ["Activate an alternate path", "Increase uplink capacity"]},
    "svc-dns": {"actionType": "restart_dns_service", "risk": "low", "scenario": "dns-failure",
                "description": "Restart the 'named' DNS service on APP-01.", "alternatives": ["Fail over to secondary DNS"]},
    "server": {"actionType": "stop_runaway_process", "risk": "medium", "scenario": "server-spike",
               "description": "Terminate the runaway CPU process on APP-01 (stress-ng).",
               "alternatives": ["Scale out the web tier", "Move workload to standby node"]},
}
```
- `recommend(inc)`: حسب نوع السبب (`link` / `svc-dns` / `server`) أنشئ `Action` بـ`approvalStatus="pending"`، الحادثة ← `awaiting_approval`.
- `POST /api/actions/{id}/approve` body `{"decidedBy": "Ahmed"}`: ← `approved` ← نفّذ (`sim`: `simulator.remediate()` · `live`: `lab_client.call(f"/remediate/{scenario}")`) ← `executed` أو `failed` + `timings.decidedAt/executedAt` ← Audit.
- `POST /api/actions/{id}/reject` body `{"decidedBy": "Ahmed", "reason": "Outside change window"}`: `reason` إلزامي (≥ 5 حروف وإلا 422) ← `rejected` ← Audit ← **لا يُستدعى المختبر إطلاقًا** ← أنشئ Action جديد `pending` بنفس التوصية (عشان يقدر المهندس يعتمد لاحقًا).
- `GET /api/audit` (آخر 200 سجل).
- **مراقب التعافي** (مهمة كل ثانية): لحادثة `executed`، إذا كل أعضائها خرجوا من `detector.active` لمدة **15 ثانية متواصلة** ← `resolved` + `recoveredAt` + `history.record(root)` + احفظ `RunRow` بالمقاييس:
  - `timeToDetect = detectedAt − injectedAt`
  - `timeToRootCause = analyzedAt − injectedAt`
  - `timeToRecover = recoveredAt − injectedAt`
  - `rawAlerts`, `incidents=1`, `noiseReduction = 1 − 1/rawAlerts`, `correct = (root == expected[scenario])`
- حوّل `demo.state` ← `recovered` وبث.

### 🟨 AI — `intelligence/explain.py` (شرح مقيّد بالأدلة)
```python
import json, re
import httpx
from app.core.config import settings

TEMPLATES = {
    "link": {
        "en": "Most likely cause: congestion on {label} ({conf}% confidence). Utilization reached {util}% of a "
              "{speed} Mbps link and latency rose from {lat0} ms to {lat} ms, starting {lead}s before the "
              "service symptoms. {n} affected service(s) sit downstream of this link.",
        "ar": "السبب الأرجح: ازدحام على الرابط {label} بثقة {conf}%. وصل الاستخدام إلى {util}% من سعة {speed} Mbps "
              "وارتفع زمن التأخير من {lat0} ms إلى {lat} ms، وبدأ ذلك قبل أعراض الخدمات بـ{lead} ثانية. "
              "عدد الخدمات المتأثرة الواقعة خلف هذا الرابط: {n}.",
    },
    # "svc-dns" و "server" بنفس الأسلوب
}
NUM = re.compile(r"\d+(?:\.\d+)?")

def grounded(text: str, facts: dict) -> bool:
    """يرفض أي رقم في النص غير موجود في الحقائق المقاسة — حماية من الهلوسة."""
    norm = lambda n: f"{float(n):g}"                      # "97.0" و "97" نفس الرقم
    allowed = {norm(n) for n in NUM.findall(json.dumps(facts))}
    return all(norm(n) in allowed for n in NUM.findall(text))

def template(kind: str, facts: dict) -> dict:
    t = TEMPLATES[kind]
    return {"en": t["en"].format(**facts), "ar": t["ar"].format(**facts), "source": "template"}

async def explain(kind: str, facts: dict) -> dict:
    base = template(kind, facts)
    if not settings.llm_enabled or not settings.anthropic_api_key:
        return base
    prompt = ("Rewrite this incident explanation for a NOC engineer in 2 short sentences. Use ONLY the facts in the "
              f"JSON; do not add any number that is not in it. Use Western digits.\nFACTS: {json.dumps(facts)}\n"
              f"DRAFT: {base['en']}")
    try:
        async with httpx.AsyncClient(timeout=4.0) as c:
            r = await c.post("https://api.anthropic.com/v1/messages",
                             headers={"x-api-key": settings.anthropic_api_key, "anthropic-version": "2023-06-01",
                                      "content-type": "application/json"},
                             json={"model": settings.llm_model, "max_tokens": 200,
                                   "messages": [{"role": "user", "content": prompt}]})
            r.raise_for_status()
            text = "".join(b.get("text", "") for b in r.json()["content"])
        if grounded(text, facts):
            return {**base, "en": text.strip(), "source": "llm"}
    except Exception:
        pass
    return base                                    # القالب هو المسار الأساسي دائمًا
```
> مرجع الـAPI: https://docs.claude.com/en/api/overview — والـLLM **اختياري** ويبقى `LLM_ENABLED=0` افتراضيًا. العرض لازم ينجح بدون إنترنت.
- `tests/test_explain.py`: `grounded("util 97%", {"util": 97})` صح؛ `grounded("util 99%", {"util": 97})` خطأ؛ القالب العربي ما فيه `{` متبقية.

### 🟦 FE — الموافقة والتدقيق
1. **`ActionCard.tsx`:** وصف التوصية + Risk chip (low أخضر/medium أصفر/high أحمر) + البدائل كقائمة صغيرة + ملاحظة ثابتة: *«No change is applied without engineer approval»* + زرين: `Approve Remediation` (أخضر، أساسي) و`Reject` (ثانوي).
   - بعد Approve: الزر يتحول لـ«Executing on R1…» بـspinner ← «Executed ✓» ← «Recovering…» ← عند `resolved` بانر أخضر.
2. **`RejectDialog.tsx`:** Modal بحقل سبب إلزامي (Placeholder: *Outside change window*) + زر تأكيد disabled حتى ≥ 5 حروف. (بدون `<form>` — `onClick` مباشر.)
3. **حقل «Engineer name»** في Settings (يُحفظ في الذاكرة فقط) ويُرسل كـ`decidedBy`.
4. **`pages/AuditPage.tsx`:** جدول (الوقت، المنفذ، الإجراء، الهدف، التفاصيل) من `GET /api/audit` مع تحديث كل 5 ثواني.
5. **Timeline كامل:** مراحل `Injected ▲ · First anomaly ● · Incident opened ● · Root cause ◆ · Rejected ✕ · Approved ✓ · Executed ⚙ · Recovered ★` بألوانها وأوقاتها النسبية (`+0s, +3s, +5s, +11s ...`).
6. **الشرح:** كتلة تحت السبب الجذري تعرض `explanation.en` أو `.ar` حسب لغة الواجهة + شارة صغيرة `template` أو `LLM · grounded ✓`.
7. **لحظة التعافي:** لما تصير `resolved`: الروابط ترجع خضراء تدريجيًا (transition 1.2s على `stroke`) + KPI MTTD/MTTR تتحدث بأنيميشن عدّاد.

### ✅ معايير قبول اليوم 8 — 🎯 M3
- [ ] Reject بدون سبب ← `422`. Reject بسبب ← `GET /api/audit` فيه السجل، و(live) `show policy-map interface Gi0/0` **ما زال** `UPLINK-SHAPE`.
- [ ] Approve (live) ← خلال ≤ 10 ثواني `show policy-map interface Gi0/0` يعرض `UPLINK-QOS` مع عدّادات `BULK` تتزايد drops، والـlatency على الرابط ترجع < 10ms، والحادثة `resolved` خلال ≤ 45 ثانية.
- [ ] `GET /api/incidents/{id}` فيه كل الأوقات: `injectedAt, detectedAt, analyzedAt, decidedAt, executedAt, recoveredAt`.
- [ ] `SELECT scenario, metrics FROM runs;` (عبر `docker compose exec db psql -U rootiq -c ...`) فيه صف لكل تشغيل.
- [ ] نفس الحلقة في sim تنجح.
- [ ] `pytest -q` أخضر · `npm test` أخضر.
- [ ] فيديو `docs/progress/m3.mp4` للحلقة كاملة.
- [ ] `git tag day-08 m3`

---

# اليوم 9 — السيناريو 2 و3 + لحظة «الواو»

**الهدف:** الثلاث سيناريوهات تنجح من أولها لآخرها (live + sim)، والشاشة تبرز القيمة بأرقام: عاصفة التنبيهات، ساعة الـMTTD، نسبة تقليل الضجيج.

### 🟨 AI — الضبط والنموذج متعدد المتغيرات
1. شغّل كل سيناريو 3 مرات live وتأكد إن السبب الأول صحيح. أي خطأ ← عدّل **العتبات أو الأوزان** فقط (لا تضف قواعد خاصة بالسيناريو!) وسجّل التغيير في `docs/RESULTS.md`.
2. **`intelligence/anomaly.py` — Isolation Forest** (المذكور في الـdeck والـdocx):
```python
import json
from pathlib import Path
import joblib, numpy as np
from sklearn.ensemble import IsolationForest

FEATURES = ["link-r1-sw1|link_utilization", "link-r1-sw1|link_latency_ms", "link-r1-sw1|link_packet_loss",
            "svc-web|http_latency_ms", "svc-dns|dns_latency_ms", "app01|cpu_percent"]
MODEL = Path("data/models/iforest.joblib")

def vectors_from_recording(path: str, step_s: float = 2.0) -> np.ndarray:
    last: dict[str, float] = {}; rows = []; t_next = None
    for line in Path(path).read_text().splitlines():
        e = json.loads(line); key = f'{e["sourceId"]}|{e["metric"]}'
        last[key] = e["value"]; t = e["ts"]
        if t_next is None: t_next = t + step_s
        if t >= t_next and all(f in last for f in FEATURES):
            rows.append([last[f] for f in FEATURES]); t_next = t + step_s
    return np.array(rows)

def train(healthy_path: str):
    X = vectors_from_recording(healthy_path)
    m = IsolationForest(n_estimators=200, contamination=0.01, random_state=7).fit(X)
    MODEL.parent.mkdir(parents=True, exist_ok=True); joblib.dump(m, MODEL)
    return len(X)

class MultivariateScorer:
    def __init__(self):
        self.m = joblib.load(MODEL) if MODEL.exists() else None
    def score(self, metrics: dict[str, dict[str, float]]) -> float | None:
        if not self.m: return None
        x = [metrics.get(f.split("|")[0], {}).get(f.split("|")[1], 0.0) for f in FEATURES]
        return float(np.clip(-self.m.decision_function([x])[0] * 4 + 0.5, 0, 1))   # 0 طبيعي … 1 شاذ جدًا
```
```bash
cd backend && python -c "from app.intelligence.anomaly import train; print(train('data/recordings/<date>-healthy-15m.jsonl'))"
```
   - في التحليل: لو `score > 0.6` أضف دليل: *«Multivariate anomaly score 0.83 (Isolation Forest trained on 15 min of healthy lab data)»*. **النموذج دليل مساند، مو صاحب القرار** — هذا بالضبط منطق «Hybrid» في الوثيقة.
3. **اختبار الإيجابيات الكاذبة (Soak):** 30 دقيقة live بدون أي حقن ← **0 حوادث**. لو ظهرت حادثة: ارفع `warmup` أو عتبة `z`.

### 🟩 BE
- توصيات DNS وCPU تشتغل live (`systemctl start named` · `pkill -f stress-ng`).
- `GET /api/runs` يرجع كل التشغيلات + ملخص: `{runs:[...], summary:{count, top1Accuracy, avgTimeToRootCause, avgNoiseReduction}}`.
- `demo.expected = {"uplink-congestion": "link-r1-sw1", "dns-failure": "svc-dns", "server-spike": "app01"}` لحساب `correct`.

### 🟦 FE — لحظة الواو
1. **`components/demo/AlertStorm.tsx`** — يستبدل عمود Raw alerts وقت الحادثة:
   - يسار: «**Traditional NMS**» + عدّاد ضخم `23 alerts` + التنبيهات تتساقط.
   - سهم متحرك ←
   - يمين: «**RootIQ**» + `1 incident` + اسم السبب.
   - تحتهم: **`Noise reduction 95.7%`** (= `1 − incidents/rawAlerts`).
2. **`components/demo/MttdStopwatch.tsx`:** يبدأ من `demo.injectedAt` (يحدث كل 100ms بـ`requestAnimationFrame`) ويتجمد عند `timings.analyzedAt` ويتحول أخضر مع نص `Root cause in 11.4 s · target < 60 s`.
3. أيقونات ونصوص خاصة بكل سيناريو في لوحة الحادثة (Network / DNS / Server).
4. **Services panel:** عند فشل DNS، شريحة `Web Application` تكتب «impacted via DNS dependency» (من `suppressedBy`).

### ✅ معايير قبول اليوم 9
- [ ] 9 تشغيلات live (3×3) ← `curl -s localhost:8000/api/runs | python3 -m json.tool` يظهر `top1Accuracy = 1.0` و`avgTimeToRootCause < 60`.
- [ ] Soak 30 دقيقة ← `0` حوادث.
- [ ] الساعة تتوقف عند وصول السبب، والـNoise reduction ≥ 80% في السيناريو 1.
- [ ] Reject ثم Approve ينجح في السيناريوهات الثلاث.
- [ ] `git tag day-09`

---

# اليوم 10 — التميّز (Arabic-first · Replay · Analytics · Presenter)

**الهدف:** الإضافات اللي تخلي الحكام يتذكرونكم بعد 20 فريق.

### 🟦 FE
1. **العربية RTL** — `src/i18n/index.ts`:
```ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './en.json';
import ar from './ar.json';

i18n.use(initReactI18next).init({ resources: { en: { translation: en }, ar: { translation: ar } },
  lng: 'en', fallbackLng: 'en', interpolation: { escapeValue: false } });
i18n.on('languageChanged', (lng) => {
  document.documentElement.lang = lng;
  document.documentElement.dir = lng === 'ar' ? 'rtl' : 'ltr';
});
export default i18n;
```
   - كل نصوص الواجهة بـ`t('incident.rootCause')`. أسماء المنافذ والمقاييس والـIPs تبقى إنجليزي داخل `<bdi>` حتى ما ينقلب ترتيبها.
   - استخدم خصائص Tailwind المنطقية (`ms-*`, `me-*`, `ps-*`, `start-*`) بدل `ml/mr/left/right` في كل الـLayout.
   - الخريطة تبقى `dir="ltr"` (مسوّاة من يوم 2).
   - الشرح يستخدم `explanation.ar` تلقائيًا.
   - خط عربي: `IBM Plex Sans Arabic` (حمّله محليًا في `public/fonts/` — **لا تعتمد على الإنترنت يوم العرض**).
2. **Incident Replay:** زر ▶ في صفحة الحادثة يعيد تشغيل الـTimeline بسرعة 5×: كل خطوة تبرز عنصرها في الخريطة وتعرض القيمة وقتها (من `GET /api/incidents/{id}/replay` = الأدلة + التنبيهات + المراحل مرتبة زمنيًا).
3. **`pages/AnalyticsPage.tsx`:**
   - بطاقات: `Top-1 accuracy 9/9` · `Avg time to root cause` · `Avg noise reduction` · `Runs`.
   - `BarChart` (Recharts) لزمن الوصول للسبب لكل تشغيل + `ReferenceLine y={60}` مكتوب عليها «Target».
   - جدول التشغيلات.
4. **Presenter Mode (`Shift+P`):** يخفي الـSidebar وأدوات التطوير، يكبّر الخط 115%، يثبّت الـStopwatch والـAlertStorm في الأعلى، ويخفي مؤشر الماوس بعد 3 ثواني سكون.
5. **الصقل:** Empty state («All systems healthy — no active incidents» مع أيقونة درع خضراء) · Loading skeletons · Error boundary يعرض «Reconnecting…» بدل شاشة بيضاء · Favicon + عنوان التبويب يتغير لـ`● 1 incident` وقت الحادثة.

### 🟩 BE
- `GET /api/incidents/{id}/replay`.
- `POST /api/demo/mode` `{"mode":"sim"|"live"}` — **تبديل ساخن**: يوقف/يشغّل المحاكي، يعمل Reset، يبث `demo` و`snapshot` جديد. (هذا منقذ يوم العرض.)
- حماية: Rate-limit بسيط على `/api/events*` (≤ 50 طلب/ثانية) ورفض أي `timestamp` أبعد من 5 دقائق عن الوقت الحالي.

### 🟨 AI
- **معايرة الثقة:** من 9+ تشغيلات احسب: هل الثقة المعروضة ≥ 0.8 لما يكون السبب صحيح؟ وجرّب حالتين «مخلوطتين» (DNS + CPU مع بعض في sim) وتأكد إن الثقة تنزل وتظهر حالة `needsInvestigation` أو يظهر المرشحين الاثنين بفارق بسيط.
- قوالب الشرح العربية للسيناريوهات الثلاثة، يراجعها أحد يكتب عربي فصيح.

### ✅ معايير قبول اليوم 10
- [ ] زر اللغة يقلب الواجهة كاملة RTL بدون أي عنصر مكسور (راجع الـ7 صفحات بلقطات شاشة في `docs/progress/rtl/`).
- [ ] Replay يشتغل لحادثة محفوظة من أمس.
- [ ] صفحة Analytics تعرض أرقام حقيقية من `runs`.
- [ ] `POST /api/demo/mode {"mode":"sim"}` أثناء live ← الواجهة تتحول خلال ≤ 3 ثواني والشارة تتغير، بدون Refresh.
- [ ] `git tag day-10`

---

# اليوم 11 — التصليب والاختبارات الآلية · ❄️ Feature Freeze 22:00

**الهدف:** «يشتغل 3 مرات متتالية من حالة نظيفة» — مثبت بسكربت، مو بالكلام.

### 🟦 FE — اختبار E2E للديمو كامل
**`frontend/playwright.config.ts`**
```ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: 'e2e', timeout: 180_000, retries: 0,
  use: { baseURL: 'http://localhost:5173', viewport: { width: 1920, height: 1080 }, video: 'retain-on-failure' },
});
```
**`frontend/e2e/demo.spec.ts`**
```ts
import { test, expect } from '@playwright/test';

for (const run of [1, 2, 3]) {
  test(`full demo loop — run ${run}`, async ({ page, request }) => {
    await request.post('/api/demo/reset');
    await page.goto('/');
    await expect(page.getByText('All systems healthy')).toBeVisible({ timeout: 30_000 });

    await page.keyboard.press('Shift+Digit1');
    await expect(page.getByTestId('root-cause')).toContainText('R1 Gi0/0', { timeout: 60_000 });
    await expect.poll(() => page.getByTestId('evidence-item').count()).toBeGreaterThanOrEqual(2);

    await page.getByRole('button', { name: 'Reject' }).click();
    await page.getByPlaceholder('Outside change window').fill('Outside change window');
    await page.getByRole('button', { name: 'Confirm reject' }).click();
    await expect(page.getByTestId('timeline')).toContainText('Rejected');

    await page.getByRole('button', { name: 'Approve Remediation' }).click();
    await expect(page.getByTestId('incident-status')).toHaveText(/resolved/i, { timeout: 90_000 });
  });
}
```
```bash
cd frontend && npx playwright install chromium
ROOTIQ_MODE=sim ../scripts/dev.sh &      # في طرفية ثانية
npx playwright test --workers=1
```
> أضف `data-testid` المطلوبة (`root-cause`, `evidence-item`, `timeline`, `incident-status`) في الكومبوننتات.

### 🟩 BE + ⬜ — البناء الإنتاجي والفحص المسبق
**`frontend/Dockerfile`**
```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
COPY configs ../configs
RUN npm run build

FROM nginx:1.27-alpine
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
```
**`frontend/nginx.conf`**
```nginx
server {
  listen 80;
  root /usr/share/nginx/html;
  location / { try_files $uri /index.html; }
  location /api/ { proxy_pass http://backend:8000; }
  location /ws/ {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
  }
}
```
أضف للـ`docker-compose.yml`:
```yaml
  frontend:
    build: { context: ., dockerfile: frontend/Dockerfile }
    ports: ["8080:80"]
    depends_on: [backend]
```
**`scripts/preflight.sh`** (يُشغّل قبل كل بروفة وقبل العرض)
```bash
#!/usr/bin/env bash
set -uo pipefail
ok(){ printf "  \033[32m✔\033[0m %s\n" "$1"; }; bad(){ printf "  \033[31m✘\033[0m %s\n" "$1"; FAIL=1; }
FAIL=0; COLLECTOR=${COLLECTOR:-192.168.100.50}
echo "RootIQ preflight"
curl -sf localhost:8000/api/health >/dev/null && ok "backend" || bad "backend"
curl -sf localhost:8080 >/dev/null && ok "frontend (8080)" || bad "frontend"
docker compose ps db | grep -q healthy && ok "postgres" || bad "postgres"
curl -sf -m 3 http://$COLLECTOR:9000/health >/dev/null && ok "lab-agent" || bad "lab-agent (use sim)"
MODE=$(curl -s localhost:8000/api/health | python3 -c "import sys,json;print(json.load(sys.stdin)['mode'])")
ok "mode = $MODE"
N=$(curl -s localhost:8000/api/incidents | python3 -c "import sys,json;print(len([i for i in json.load(sys.stdin) if i['status']!='resolved']))")
[ "$N" = "0" ] && ok "no open incidents" || bad "$N open incidents → run scripts/demo-reset.sh"
[ -f docs/demo-backup.mp4 ] && ok "backup video present" || bad "backup video missing"
exit $FAIL
```
**`scripts/demo-reset.sh`**: `curl -s -X POST localhost:8000/api/demo/reset && sleep 20 && ./scripts/preflight.sh`

### 🟥 INFRA
- **EVE-NG snapshot:** بعد ما يكون كل شي طبيعي: أوقف العقد ← انسخ مجلد المختبر `/opt/unetlab/tmp/0/<lab-uuid>/` إلى `/root/rootiq-golden/` (استرجاعه = نسخ عكسي). وثّق الأمرين في `README.md`.
- ترتيب الإقلاع الموثّق: R1 → SW1/SW2 (انتظر 90 ث) → APP-01 → COLLECTOR-01 ← تأكد من `systemctl status rootiq-collector rootiq-lab-agent`.
- اختبار **بدون إنترنت**: افصل WiFi اللابتوب كامل وشغّل الحلقة ← لازم تنجح.

### ✅ معايير قبول اليوم 11
- [ ] `npx playwright test` → **3 passed** (sim).
- [ ] نفس الحلقة يدويًا live ×3 متتالية بدون أي تدخل غير الـReset.
- [ ] `docker compose up -d --build && ./scripts/preflight.sh` كله ✔ (عدا الفيديو).
- [ ] الحلقة تنجح والإنترنت مفصول.
- [ ] استهلاك: `docker stats --no-stream` backend < 400MB RAM.
- [ ] 🔒 **Feature Freeze**: بعد 22:00 ممنوع أي ميزة جديدة — إصلاحات فقط بـPR يراجعه اثنين.
- [ ] `git tag day-11 v1.0-rc1`

---

# اليوم 12 — القصة والعرض والأرقام

**الهدف:** العرض التقديمي يعكس **نتائج مقاسة** مو «أهداف»، والقصة محفوظة.

### ⬜ ALL
1. **`docs/RESULTS.md`** — من `GET /api/runs`:
   | المقياس | الهدف في الـDeck | المقاس فعليًا |
   |---|---|---|
   | زمن الحادثة المترابطة | < 60 ث | __ ث (متوسط 9 تشغيلات live) |
   | ترتيب السبب | Top 3 | Top-1 صحيح __/9 |
   | تقليل التنبيهات المكررة | 30% | __% |
   | موافقة بشرية قبل العلاج | 100% | 100% (مسجل في Audit) |
2. **تحديث الـDeck (`RootIQ_Pitch_Deck_Final.pptx`):**
   - شريحة 8 (Demo): أضف لقطة شاشة حقيقية من الخريطة وقت الحادثة.
   - شريحة 9 (Value): حوّل «Pilot targets» إلى «**Measured in our lab**» بالأرقام الحقيقية.
   - أضف شريحة «Why RootIQ is explainable»: لقطة CandidateRanking + Grounded explanation.
   - أضف شريحة Architecture محدثة من `docs/ARCHITECTURE.md`.
3. **فيديو احتياطي v1:** OBS بدقة 1920×1080، 5 دقائق، نفس سكربت العرض، صوت واضح ← `docs/demo-backup.mp4` (+ نسخة على USB + Google Drive).
4. **`README.md`:** سطر القيمة · لقطة GIF · Quick start (3 أوامر) · المعمارية · أوضاع sim/live · النتائج · الفريق.
5. **`docs/ARCHITECTURE.md`** بمخطط Mermaid:
```mermaid
flowchart LR
  subgraph Lab[EVE-NG lab]
    R1 --- SW1 --- APP01[APP-01 DNS+Web]
    R1 --- SW2 --- COL[COLLECTOR-01]
  end
  COL -- SNMP/ICMP/DNS/HTTP/Syslog --> C[Collector]
  C -- normalized events --> API[FastAPI ingest]
  API --> ST[State + Detector] --> COR[Correlator] --> RCA[RCA ranker + Graph] --> EXP[Explanation]
  EXP --> WS((WebSocket)) --> UI[React dashboard]
  UI -- approve/reject --> ACT[Action service] -- whitelisted --> AG[Lab agent] --> R1
  API --> PG[(PostgreSQL)]
```
6. كتابة **`docs/DEMO_SCRIPT.md`** و**`docs/QA_BANK.md`** (المحتوى في الملحق أ وب أدناه) وتوزيع الأدوار في العرض.

### ✅ معايير قبول اليوم 12
- [ ] كل رقم في الـDeck له مصدر في `docs/RESULTS.md`.
- [ ] الفيديو الاحتياطي ≤ 5:00 ومحفوظ في 3 أماكن.
- [ ] كل عضو يقدر يشرح المعمارية في 30 ثانية.
- [ ] `git tag day-12`

---

# اليوم 13 — البروفة النهائية وتدريبات الطوارئ

**الهدف:** العرض يصير «ذاكرة عضلية»، وكل عطل محتمل له خطة مجرّبة.

### ⬜ ALL — الجدول
| الوقت | النشاط |
|---|---|
| 09:00 | إقلاع كامل من الصفر على **نفس اللابتوب والشاشة والشبكة** اللي بتستخدمونها في المكان + `preflight.sh` |
| 09:30 | بروفة 1 كاملة (Pitch + Demo + أسئلة) مع ساعة إيقاف · تسجيل ملاحظات |
| 10:30 | إصلاح ملاحظات بروفة 1 (نصوص/ترتيب فقط) |
| 11:30 | بروفة 2 |
| 13:30 | **تدريبات الطوارئ** (تحت) |
| 15:30 | بروفة 3 أمام شخص من خارج الفريق يلعب دور حكم ويسأل من `QA_BANK.md` |
| 17:00 | تسجيل الفيديو الاحتياطي النهائي v2 |
| 18:00 | تجهيز الشنطة (الملحق هـ) |

### تدريبات الطوارئ (كل واحد لازم ينجح في < 30 ثانية بدون ارتباك)
| العطل المفتعل | الاستجابة المتدربة |
|---|---|
| EVE-NG يعلق وسط العرض | المقدّم يقول «Let me switch to our recorded lab feed» ← `POST /api/demo/mode {"mode":"sim"}` (زر في Settings) ← يكمل. الشارة تكتب SIMULATION بصراحة. |
| الـWiFi في المكان مقطوع | لا شي — كل شي محلي. (تأكدتوا يوم 11) |
| الباك إند انهار | `docker compose restart backend` (الواجهة تعيد الاتصال لحالها) |
| اللابتوب نفسه طاح | اللابتوب الثاني (مجهز بنفس الريبو + Docker + الفيديو) أو تشغيل الفيديو مباشرة |
| الحكم يطلب سيناريو غير الأول | `Shift+R` ثم `Shift+2` (مجرّب) |
| الـRCA طلع غلط (نظريًا) | المقدّم يفتح CandidateRanking ويقول «This is exactly why we show evidence and confidence instead of a black-box answer» ← ثم يعيد الحقن |

### ✅ معايير قبول اليوم 13
- [ ] 3 بروفات كاملة، كل واحدة ≤ الوقت المسموح (Pitch + Demo).
- [ ] كل تدريبات الطوارئ نجحت مرة على الأقل.
- [ ] الفيديو v2 جاهز في 3 أماكن.
- [ ] `git tag v1.0` — هذا اللي يُعرض.

---

# اليوم 14 — يوم العرض (Runbook)

| الوقت | الإجراء | المسؤول |
|---|---|---|
| T−120 د | الوصول، توصيل الشاشة/HDMI، اختبار الدقة 1920×1080 والتكبير 100% | Presenter |
| T−90 د | إقلاع EVE-NG بالترتيب الموثق (R1 → SW → APP-01 → COLLECTOR-01) | INFRA |
| T−60 د | `docker compose up -d` ← `./scripts/preflight.sh` كله ✔ | BE |
| T−45 د | تشغيل تجريبي كامل مرة وحدة (live) ثم `./scripts/demo-reset.sh` | FE (أنت) |
| T−30 د | تعطيل الإشعارات (Do Not Disturb)، إغلاق كل التبويبات عدا 2: الـDashboard (Presenter Mode) والـDeck | Presenter |
| T−15 د | Baseline يسخن 10 دقائق بدون لمس (مهم للكاشف) — **لا تحقنوا شي** | ALL |
| T−5 د | `preflight.sh` أخير · الفيديو الاحتياطي مفتوح في تبويب مخفي | FE |
| T | العرض حسب `DEMO_SCRIPT.md` | Presenter + FE على الكيبورد |
| T+ | بعد العرض: لا تطفّون شي — الحكام أحيانًا يرجعون يطلبون تجربة | ALL |

---

# الملحق أ — سكربت العرض (5 دقائق للديمو)

> المقدّم يتكلم، وأنت (أحمد) على الكيبورد. كل سطر معه **الإجراء** و**الوقت التراكمي**. الأرقام بين [ ] تُستبدل بالمقاسة من `RESULTS.md`.

| الوقت | الكلام (المقدّم) | الإجراء (أحمد) |
|---|---|---|
| 0:00 | «هذي شبكة حقيقية تشتغل الحين داخل EVE-NG: راوتر، سويتشين، سيرفر DNS وتطبيق، وكولكتر RootIQ. كل شي أخضر.» | Presenter Mode مفعّل، الخريطة كاملة |
| 0:20 | «كل خط هنا مو رسمة — هو رابط بين منفذين حقيقيين. هذا R1 Gi0/0 إلى SW1 Gi0/1: السرعة، الاستخدام، التأخير، الفقد — مباشر من SNMP.» | اضغط الرابط r1-sw1 → LinkInspector |
| 0:45 | «الحين بنسوي اللي يصير كل يوم في مراكز العمليات: حركة كثيفة غير مهمة تخنق الرابط الرئيسي.» | `Shift+1` — الساعة تبدأ |
| 1:00 | «شوفوا اليسار: هذا اللي تعرضه أدوات المراقبة التقليدية — [23] تنبيه من الراوتر والتطبيق والـDNS، كل واحد لحاله. المهندس لازم يربطها بمخه.» | AlertStorm يمتلئ |
| 1:25 | «RootIQ جمّعها في حادثة **وحدة**، ورتّب الأسباب، وحدد: ازدحام على R1 Gi0/0 بثقة [91]%. الساعة وقفت عند [11] ثانية — هدفنا كان أقل من 60.» | الرابط أحمر نابض، الحلقة تمتلئ |
| 1:55 | «ليش نثق فيه؟ لأنه ما يعطيك جواب صندوق أسود. هذي الأدلة المقاسة: الاستخدام [97]% من 10 ميجا، التأخير من [2] إلى [86] ms، وبدأ قبل أعراض الخدمات بـ[6] ثواني.» | أشر على EvidenceList |
| 2:20 | «وهذي المرشحات الثانية: DNS كان شاذ — لكن النظام عرف إنه **عَرَض** لأنه واقع خلف الرابط المزدحم، فخفّض درجته. هذا فهم الطوبولوجيا، مو مجرد أرقام.» | أشر على CandidateRanking و suppressedBy |
| 2:45 | «التوصية: تطبيق سياسة QoS تحد الحركة الكبيرة. مخاطرة منخفضة. لكن RootIQ **ما ينفذ شي بدون موافقة المهندس**.» | ActionCard |
| 3:00 | «نفترض المهندس رفض لأننا خارج نافذة التغيير.» | Reject ← اكتب السبب ← Confirm |
| 3:15 | «ما تغير شي في الشبكة، والقرار انسجل بالسبب والاسم والوقت.» | Timeline يعرض Rejected |
| 3:30 | «الحين يعتمد.» | Approve Remediation |
| 3:40 | «RootIQ دخل على الراوتر وطبّق السياسة فعليًا — شوفوا التأخير ينزل والخط يرجع أخضر.» | الخريطة تتعافى |
| 4:05 | «الحادثة انحلت: الاكتشاف [5] ث، السبب [11] ث، التعافي [52] ث. وكل خطوة في سجل تدقيق.» | Timeline كامل + KPI |
| 4:25 | «وجربناه [9] مرات على 3 أنواع أعطال — شبكة، DNS، وموارد سيرفر — والسبب الأول كان صحيح [9/9]، وتقليل الضجيج [95]%.» | صفحة Analytics |
| 4:45 | «RootIQ: Find the cause before it becomes an outage.» | ارجع للخريطة الخضراء |

**قواعد ذهبية للعرض:** لا تقرأ من الشاشة · لا تقول «إن شاء الله يشتغل» · لو صار شي غير متوقع: «This is live — let me show you» ثم خطة الطوارئ · خلّ الحكام يشوفون الأرقام أكثر من الكلام.

---

# الملحق ب — بنك أسئلة الحكام (مع إجابات جاهزة)

| السؤال | الجواب المختصر |
|---|---|
| هل هذا AI حقيقي أو قواعد؟ | هجين عن قصد: Baseline إحصائي + Isolation Forest متعدد المتغيرات + Graph reasoning + ترتيب موزون قابل للتفسير. القواعد وحدها ما تعمم، والـML وحده يحتاج بيانات موسومة ما عندنا — الهجين يعطي تفسير وموثوقية ومسار تطوير. |
| كيف تتوسع لشبكة فيها آلاف الأجهزة؟ | التحليل يشتغل على «مجموعة الأعراض المرتبطة» فقط، مو الشبكة كاملة؛ الـGraph عمليات مسارات تتناسب مع حجم الحادثة. الكولكترات موزعة وتدفع صيغة موحدة. الاكتشاف التلقائي عبر CDP/LLDP في مرحلة الـPilot. |
| وش يصير لو الـRCA غلط؟ | نعرض الثقة والأدلة والمرشحين، ولو الثقة < 55% نقول صراحة «يحتاج تحقيق». وما فيه أي تنفيذ بدون موافقة بشرية. |
| ليش ما تستخدمون LLM للتحليل؟ | الـLLM للصياغة فقط، ومقيد: أي رقم ما هو موجود في الأدلة المقاسة يرفضه النظام ويرجع للقالب. التحليل نفسه حتمي وقابل للتدقيق. |
| الفرق عن Datadog / Dynatrace / Splunk ITSI؟ | Vendor-neutral وخفيف ويشتغل على البيئات الهجينة والشبكات التقليدية (SNMP/Syslog) — مو بس Cloud APM — ويربط المنافذ الفيزيائية بالخدمات، مع دورة موافقة مدمجة. ونشر خاص (Private deployment) مناسب لمتطلبات سيادة البيانات في السعودية. |
| كيف تتعلم مع الوقت؟ | كل حادثة تنحل بموافقة تزيد `historical_support` للسبب — شفتوه في التشغيل الثالث ارتفعت الثقة. لاحقًا: تعلّم الأوزان من الحوادث المحلولة. |
| الأمان؟ | حسابات قراءة فقط لـSNMP، الوكيل ينفذ Whitelist ثابتة فقط، الأسرار في Environment، كل قرار في Audit Log، وضع محاكاة كامل. |
| نموذج العمل؟ | اشتراك حسب عدد الأصول المراقبة + تكامل مؤسسي + نشر خاص. العملاء الأوائل: NOCs المؤسسية، مزودي الخدمات المُدارة، فرق مراكز البيانات والسحابة. |
| وش الخطوة الجاية؟ | Pilot مع NOC حقيقي: اكتشاف تلقائي، SNMP على نطاق واسع، RBAC، تكامل ITSM، ثم تنبؤ بالسعة وتحليل أثر التغييرات. |
| البيانات حقيقية ولا مصطنعة؟ | الديمو live من مختبر حقيقي بأجهزة Cisco افتراضية وحركة iperf3 حقيقية. وضع المحاكاة موجود كاحتياط ومكتوب على الشاشة بوضوح لو استخدمناه. |

---

# الملحق ج — سجل المخاطر مع «مُحفّز التفعيل»

| الخطر | علامة الإنذار المبكر | الإجراء | آخر موعد للقرار |
|---|---|---|---|
| EVE-NG ما يتحمل | العقد تاخذ > 5 د للإقلاع أو CPU > 90% | قلّل RAM للسويتشات، أو استبدل vIOS-L2 بـLinux bridge، أو جهاز أقوى | نهاية اليوم 2 |
| SNMP ما يعطي أرقام | `snmpget` يفشل | Netmiko `show interfaces` + parse كبديل | نهاية اليوم 4 |
| الازدحام ما يسبب latency واضح | فرق القفزات < 20ms | خفّض الـshaper إلى 5M أو ارفع iperf إلى 25M | اليوم 5 |
| RCA يخطئ في سيناريو | Top-1 ≠ المتوقع في أي تشغيل | عدّل الأوزان/العتبات + أضف اختبار fixture | اليوم 9 |
| الواجهة بطيئة | < 30 FPS وقت الحادثة | خنق التحديثات 1Hz، `React.memo` للعقد، أوقف الأنيميشن للروابط السليمة | اليوم 10 |
| الـLLM بطيء/مقطوع | > 4 ث | القالب هو الأساسي أصلًا — `LLM_ENABLED=0` يوم العرض إلا لو الإنترنت مضمون | اليوم 11 |
| تأخر عام في الخطة | معلَم M2 ما تحقق نهاية اليوم 7 | **فعّل خطة الـ7 أيام** من اليوم 8: ألغِ Replay والـIsolation Forest والعربية | اليوم 7 |

---

# الملحق د — ضغط الخطة

### نسخة 7 أيام
| اليوم | يجمع أيام الخطة الكاملة | ما يُحذف |
|---|---|---|
| 1 | 0 + 1 + 2 | — |
| 2 | 3 + 4 | Devices page، Syslog |
| 3 | 5 + 6 | Persistence في DB (خلّها ذاكرة + JSON) |
| 4 | 7 | Recorder/Replay |
| 5 | 8 + 9 (سيناريو DNS فقط كثاني) | Isolation Forest، سيناريو CPU |
| 6 | 11 + 12 | العربية، Replay، Analytics (يكفي جدول) |
| 7 | 13 + 14 | — |

### نسخة 48 ساعة (هاكاثون في الموقع)
| الساعات | المهمة |
|---|---|
| 0–4 | ريبو + topology.json + React Flow بمنافذ + FastAPI + Simulator |
| 4–10 | WS + Store + حقن (sim) + التنبيهات الخام |
| 10–16 | Detector + Correlator + RCA + لوحة الحادثة |
| 16–22 | Approve/Reject + Recovery + Timeline + AlertStorm + Stopwatch |
| 22–28 | نوم إلزامي 6 ساعات (بالتناوب) |
| 28–36 | المختبر live (لو جاهز مسبقًا) + ربط الكولكتر + سيناريو 1 live |
| 36–42 | تصليب + Playwright + فيديو احتياطي |
| 42–48 | Deck بالأرقام + 3 بروفات |
> في نسخة 48 ساعة: **جهّزوا مختبر EVE-NG كامل قبل الهاكاثون** إذا القوانين تسمح بتجهيز البيئة مسبقًا.

---

# الملحق هـ — قائمة التحقق النهائية + الشنطة

### قائمة البناء (من ملحق A في الوثيقة، موسّعة)
- [ ] الريبو فيه `backend` و`frontend` و`configs` و`lab` و`docs`.
- [ ] مختبر EVE-NG يقلع من Snapshot محفوظ.
- [ ] `topology.json` فيه الأجهزة والمنافذ والروابط والخدمات.
- [ ] React Flow يعرض الطوبولوجيا بأسماء المنافذ الصحيحة.
- [ ] الكولكتر يرسل أحداث موحدة.
- [ ] الواجهة تستقبل تحديثات WebSocket.
- [ ] حقن الازدحام قابل للتكرار.
- [ ] تجميع الحوادث وترتيب الأسباب يشتغل.
- [ ] الأدلة تظهر في لوحة الحادثة.
- [ ] الموافقة والرفض مسجلين.
- [ ] التعافي واضح على الخريطة.
- [ ] وضع الاحتياط يشتغل بدون إنترنت.
- [ ] الفريق تدرب على القصة (5 دقائق) 3 مرات.
- [ ] (إضافي) 3 سيناريوهات · AlertStorm · Stopwatch · Analytics · العربية · Playwright ×3 · preflight.

### الشنطة
لابتوب العرض + الشاحن · لابتوب احتياطي بنفس الريبو وDocker والفيديو · محوّل HDMI/USB-C (اثنين) · موزّع كهرباء · ماوس · Clicker للشرائح · USB فيه: الفيديو + الـDeck (PPTX + PDF) + الريبو zip · نسخة مطبوعة من سكربت العرض وبنك الأسئلة · ماء 😄

---

# الملحق و — لو الفريق صغير (أو أنت لحالك)

ترتيب الأولوية (لا تنتقل للسطر اللي بعده قبل ما يكتمل اللي قبله):
1. 🟦 الخريطة بالمنافذ (اليوم 1–2) — **هذا وجه المنتج**.
2. 🟩 Simulator + WS + Store (اليوم 3).
3. 🟨 Detector + Correlator + RCA بالاختبارات (اليوم 5–7).
4. 🟦 لوحة الحادثة + Approve/Reject + Timeline (اليوم 6–8).
5. 🟦 AlertStorm + Stopwatch (اليوم 9) — لحظة الواو.
6. 🟥 المختبر live لسيناريو واحد فقط (الازدحام).
7. كل شي ثاني إضافات.

**تنبيه صريح:** المسار «Infrastructure & Cloud» والحكام غالبًا يقدّرون المختبر الحقيقي. وضع المحاكاة لحاله يقدر يوصلكم لمنتج ممتاز، لكن **سيناريو live واحد على الأقل** يرفع فرصة المركز الأول بشكل كبير — لو المختبر صعب عليك لحالك، استعن بمهندس شبكات ولو ليومين (اليوم 2 واليوم 5).

---

> **الخلاصة:** ابنِ الخريطة أولًا، خلّ رقم واحد يتحرك، ثم حادثة واحدة، ثم سبب واحد صحيح، ثم الموافقة. كل يوم ينتهي بـtag واختبارات خضراء. والعرض يُبنى على أرقام قستوها بأنفسكم. 🏆
