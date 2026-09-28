# Demo script — 5 minutes

> Presenter speaks; **Ahmed (FE)** on keyboard. Numbers in `[brackets]` come from `docs/RESULTS.md` (measured). Update brackets if RESULTS changes.

**Roles:** Presenter (voice) · FE Ahmed (hotkeys) · BE standby (`preflight` / restart) · INFRA (EVE if live)

| Time | Presenter | Action (Ahmed) |
|---|---|---|
| 0:00 | «هذي شبكة حقيقية تشتغل الحين داخل EVE-NG: راوتر، سويتشين، سيرفر DNS وتطبيق، وكولكتر RootIQ. كل شي أخضر.» | Presenter Mode on (`Shift+P`), full map healthy |
| 0:20 | «كل خط هنا مو رسمة — هو رابط بين منفذين حقيقيين. هذا R1 Gi0/0 إلى SW1 Gi0/1: السرعة، الاستخدام، التأخير، الفقد — مباشر من SNMP.» | Click link `r1–sw1` → LinkInspector |
| 0:45 | «الحين بنسوي اللي يصير كل يوم في مراكز العمليات: حركة كثيفة غير مهمة تخنق الرابط الرئيسي.» | `Shift+1` — MTTD stopwatch starts |
| 1:00 | «شوفوا اليسار: هذا اللي تعرضه أدوات المراقبة التقليدية — [~33] تنبيه من الراوتر والتطبيق والـDNS، كل واحد لحاله. المهندس لازم يربطها بمخه.» | AlertStorm fills |
| 1:25 | «RootIQ جمّعها في حادثة **وحدة**، ورتّب الأسباب، وحدد: ازدحام على R1 Gi0/0 بثقة عالية. الساعة وقفت عند [~11] ثانية — هدفنا كان أقل من 60.» | Link pulses red; root-cause fills |
| 1:55 | «ليش نثق فيه؟ لأنه ما يعطيك جواب صندوق أسود. هذي الأدلة المقاسة: استخدام مرتفع، تأخير قفز، وبدأ قبل أعراض الخدمات.» | Point EvidenceList |
| 2:20 | «وهذي المرشحات الثانية: DNS كان شاذ — لكن النظام عرف إنه **عَرَض** لأنه واقع خلف الرابط المزدحم، فخفّض درجته. هذا فهم الطوبولوجيا، مو مجرد أرقام.» | CandidateRanking + `suppressedBy` |
| 2:45 | «التوصية: تطبيق سياسة QoS تحد الحركة الكبيرة. مخاطرة منخفضة. لكن RootIQ **ما ينفذ شي بدون موافقة المهندس**.» | ActionCard |
| 3:00 | «نفترض المهندس رفض لأننا خارج نافذة التغيير.» | Reject → reason `Outside change window` → Confirm |
| 3:15 | «ما تغير شي في الشبكة، والقرار انسجل بالسبب والاسم والوقت.» | Timeline shows **Rejected** |
| 3:30 | «الحين يعتمد.» | Approve Remediation |
| 3:40 | «RootIQ دخل على الراوتر وطبّق السياسة فعليًا — شوفوا التأخير ينزل والخط يرجع أخضر.» | Map recovers |
| 4:05 | «الحادثة انحلت: الاكتشاف ثم السبب ثم التعافي — وكل خطوة في سجل تدقيق.» | Timeline + KPI strip |
| 4:25 | «وجربناه [9] مرات على 3 أنواع أعطال — شبكة، DNS، وموارد سيرفر — والسبب الأول كان صحيح [9/9]، وتقليل الضجيج [96%].» | Analytics page |
| 4:45 | «RootIQ: Find the cause before it becomes an outage.» | Back to green map |

## Golden rules

- Do not read the screen · never say «إن شاء الله يشتغل»
- Unexpected blip: «This is live — let me show you» → day-13 failover
- Judges should see numbers more than talk

## Pre-demo

```bash
./scripts/preflight.sh   # all ✔ except optional backup video
./scripts/demo-reset.sh
```
