# RootIQ — نظام التصميم والهوية البصرية (v1.0)

> نظام تصميم كامل يعيد بناء واجهة RootIQ: الألوان، الخطوط، الشكل، الحركة، النصوص، والشعار.
> مبني على دليل الشاشات `UI.md` (8 صفحات + الإطار المشترك + لوحة الحادثة).
> افتح `preview.html` في المتصفح لترى كل شيء مطبّقًا على شاشة Operations (أضف `?theme=light&lang=en` للتبديل).

**افتراض يجب أن تعرفه:** لم أرَ كود `frontend/`، فقط `UI.md`. لذلك كل خطوات التنفيذ أدناه تفترض Vite + React + TypeScript (استنتاجًا من `frontend/src/App.tsx`). إن كان عندك إعداد مختلف فالتوكنز والشعار يعملان كما هما، وتتغير فقط سطور الاستيراد في اليوم الأول.

---

## 0. محتويات الحزمة

```
rootiq-brand/
├── BRAND-IDENTITY.md        هذا الملف
├── tokens.css               مصدر الحقيقة: ألوان، خطوط، مسافات، حركة (داكن + فاتح)
├── Logo.tsx                 مكوّنان: RootIQMark و RootIQLogo
├── check-contrast.mjs       فحص آلي لنسب التباين من tokens.css
├── preview.html             معاينة حيّة (RTL/LTR، داكن/فاتح)
└── logo/
    ├── rootiq-mark.svg                  الرمز، للخلفيات الداكنة
    ├── rootiq-mark-on-light.svg         الرمز، للخلفيات الفاتحة
    ├── rootiq-mark-mono-white.svg       أحادي أبيض (ختم، طباعة بلون واحد)
    ├── rootiq-mark-mono-ink.svg         أحادي نيلي غامق
    ├── rootiq-logo.svg                  الشعار الأفقي EN، داكن
    ├── rootiq-logo-on-light.svg         الشعار الأفقي EN، فاتح
    ├── rootiq-logo-ar.svg               الشعار الأفقي AR، داكن
    ├── rootiq-logo-ar-on-light.svg      الشعار الأفقي AR، فاتح
    ├── rootiq-app-icon.svg              أيقونة التطبيق 512×512
    └── favicon.svg                      أيقونة التبويب (نسخة أسمك)
```

---

## 1. الهوية في جملة واحدة

**RootIQ يحوّل عاصفة التنبيهات إلى سبب واحد، ويقول لك كم هو واثق منه.**

| | |
|---|---|
| الفكرة | **التقارب**: 74 تنبيهًا تتجمع في نقطة واحدة. هذه الفكرة هي الرمز، وهي الحركة الوحيدة المميزة في التطبيق |
| الشخصية | هادئ، دقيق، يعرض الدليل قبل الاستنتاج. غرفة تحكم لا لوحة تسويق |
| الشعار النصي EN | From alert storm to one root cause |
| الشعار النصي AR | من عاصفة التنبيهات إلى سبب واحد |
| الوضع الافتراضي | داكن (غرف المراقبة وشاشات العرض). الفاتح مدعوم بالكامل |

**قاعدة اللون الذهبية:** لون العلامة (الأزرق السماوي «Signal») يعني «الإشارة التي وجدت السبب» أو «شيء تفاعلي». وهو ليس لون حالة. الأحمر للعطل، الكهرماني للتأثر، الأخضر للسلامة، ولا يُستخدم أي منها للزينة.

---

## 2. الشعار

### 2.1 الفكرة

الرمز حرف **R** مرسوم كشبكة: الساق والعروة بلون النص (الشبكة)، والساق المائلة بلون Signal هي **المسار من الأعراض إلى السبب**، وتنتهي بنقطة مملوءة هي **السبب الجذري** تحيط بها حلقة خافتة. الحلقة هي نفسها حلقة الثقة (Confidence ring) في لوحة الحادثة وعلامة السبب الجذري على الخريطة، فالشعار والمنتج يتكلمان بالشكل نفسه.

### 2.2 البناء (شبكة 64×64)

| العنصر | القيمة |
|---|---|
| الساق | `M16 9 V53`، سماكة 5، أطراف دائرية |
| العروة | `H31 A12.5 12.5 0 0 1 31 34 H16`، سماكة 5 |
| الساق المائلة | `(29,34) → (44,49)`، سماكة 5، لون `--brand`، **ترسم تحت العروة** |
| العقدة | مركز `(47,52)`، نصف القطر 6 |
| الحلقة | نصف القطر 10.5، سماكة 2، شفافية 0.45 |
| نسخة الأحجام الصغيرة (≤ 28px) | السماكة 6.5، العقدة 6.5، **بدون حلقة** |

الاسم: `RootIQ` بخط Readex Pro وزن 500، تباعد −1%، وحرف R فيه هو نفسه الرمز (نفس ارتفاع الحرف الكبير ونفس سماكة الساق 12.2). النسخة العربية «روت آي كيو» بخط Readex Pro وزن 600 والرمز على اليمين (جهة البداية). **كل النصوص محوّلة إلى مسارات**، فلا تحتاج الشعارات إلى تثبيت أي خط.

> «روت آي كيو» اقتراح من عندي للنسخة العربية. إن فضّلتم اسمًا عربيًا آخر فهو تعديل سطر واحد وإعادة توليد.

### 2.3 الاستخدام

| الحالة | الملف |
|---|---|
| السايدبار، التبويب، أزرار صغيرة | `RootIQMark` من `Logo.tsx` (يقرأ الألوان من التوكنز فيتبدل مع الثيم) |
| صفحة الدخول، «حول»، العروض، المستندات | `rootiq-logo*.svg` (EN أو AR حسب لغة المحتوى) |
| وثيقة بلون واحد، ختم، فاكس | `rootiq-mark-mono-*.svg` |
| أيقونة التطبيق/PWA | `rootiq-app-icon.svg` |
| favicon | `favicon.svg` |

- **المساحة الآمنة:** حول الشعار من كل جهة ما لا يقل عن قطر الحلقة (≈ ثلث ارتفاع الرمز).
- **الحد الأدنى:** الرمز 16px (نسخة favicon) / 24px في الواجهة (تُختار النسخة الأسمك تلقائيًا ≤ 28px) / ويظهر بالحلقة من 32px. الشعار الأفقي لا يقل ارتفاعه عن 20px.
- **ممنوع:** تمطيط أو تدوير، إضافة ظل أو تدرج أو توهج، تلوين العقدة بالأحمر أو الأخضر (ألوان حالة)، استخدام نسخة الخلفية الداكنة على فاتحة أو العكس، إعادة كتابة الاسم بخط آخر، تغيير شفافية الحلقة، وضعه فوق صورة مزدحمة.

---

## 3. الألوان

عائلتان فقط: **Abyss** (نيلي عميق، الأسطح والنص) و**Signal** (سماوي، العلامة). لا تدرجات زخرفية في أي مكان.

### 3.1 الخامات (Primitives)

| Abyss | | Signal | |
|---|---|---|---|
| 950 | `#080B22` | 300 | `#7FE6FA` |
| 900 | `#0C1030` | 400 | `#3DD6F5` |
| 850 | `#11163F` | 500 | `#14B8DC` |
| 800 | `#181E52` | 600 | `#0A7C9E` |
| 700 | `#232B6A` | 700 | `#08708F` |
| 600 | `#343E86` | | |
| 500 | `#5A64A8` | | |
| 400 | `#8089C8` | | |
| 300 | `#A9B0E0` | | |
| 200 | `#CDD2F0` | | |
| 100 | `#E8EBFF` | | |
| 50 | `#F3F5FD` | | |

### 3.2 التوكنز الدلالية (هذه فقط تُستخدم في المكوّنات)

| التوكن | داكن | فاتح | الاستخدام |
|---|---|---|---|
| `--bg-canvas` | `#080B22` | `#E9EDFB` | خلفية خريطة الطوبولوجيا |
| `--bg-app` | `#0C1030` | `#F3F5FD` | خلفية التطبيق |
| `--bg-panel` | `#11163F` | `#FFFFFF` | اللوحات والجداول والشريط الجانبي |
| `--bg-raised` | `#181E52` | `#F7F8FE` | عنصر مرفوع داخل لوحة (بطاقة الإجراء، الأزرار الثانوية) |
| `--bg-float` | `rgba(17,22,63,.82)` | `rgba(255,255,255,.86)` | اللوحات العائمة فوق الخريطة (مع `backdrop-filter: blur(14px)`) |
| `--text-1` | `#E8EBFF` | `#0C1030` | العناوين والنص الأساسي |
| `--text-2` | `#A9B0E0` | `#3A4380` | نص ثانوي، تسميات |
| `--text-3` | `#8E97D4` | `#525CA0` | أدنى نص مسموح (تلميحات، تواقيت) |
| `--brand` | `#3DD6F5` | `#0A7C9E` | خلفية الزر الأساسي، العنصر النشط، حلقة الثقة |
| `--brand-text` | `#3DD6F5` | `#08708F` | روابط ونصوص بلون العلامة |
| `--ok` | `#4ADE80` | `#15803D` | سليم / تعافى |
| `--warn` | `#FFB020` | `#B45309` | متأثر / تحذير / هدف 60s |
| `--crit` | `#FF5C7A` | `#C81F45` | سبب جذري / حرج / فشل |
| `--topo-root` | = `--crit` | = `--crit` | السبب الجذري على الخريطة |
| `--topo-affected` | = `--warn` | = `--warn` | مسار التأثر |

القائمة الكاملة (حدود، حالات hover/selected، رسوم بيانية، ظلال) في `tokens.css`.

### 3.3 القواعد

1. **الحالة لا تُنقل باللون وحده أبدًا.** لكل حالة شكل ونص: ● سليم، ▲ متأثر، ◆ سبب جذري (مطبّق في `.chip` داخل `preview.html`).
2. **العلامة ≤ 5% من البكسلات:** الزر الأساسي، عنصر التنقل النشط، الروابط، حلقة التركيز، تقدّم حلقة الثقة، مؤشر Live lab.
3. **لا hex داخل المكوّنات.** كل لون عبر `var(--token)` (انظر اختبار القبول في اليوم الثاني).
4. نسب التباين محسوبة وموثّقة (WCAG 2.1) وتُفحص آليًا بـ `check-contrast.mjs`:

| الزوج | داكن | فاتح |
|---|---|---|
| `--text-1` على `--bg-panel` | 14.67 | 18.54 |
| `--text-2` على `--bg-panel` | 8.24 | 9.15 |
| `--text-3` على `--bg-raised` | 5.59 | 5.83 |
| `--brand-text` على `--bg-panel` | 10.03 | 5.64 |
| `--text-on-brand` على `--brand` | 10.72 | 4.78 |
| `--ok` / `--warn` / `--crit` على `--bg-panel` | 9.96 / 9.49 / 5.84 | 5.02 / 5.02 / 5.62 |

---

## 4. الخطوط

| الدور | الخط | لماذا |
|---|---|---|
| الواجهة كلها (عربي + لاتيني) | **Readex Pro** (متغيّر، 160–700) | الحروف اللاتينية والعربية مصممة معًا فلا يختلف خط الأساس ولا الوزن بين اللغتين، وهو مصمم للقراءة المريحة على مسافة عرض |
| كل ما يتغير مباشرة أو يُنسخ | **IBM Plex Mono** (400/500/600) | أرقام ثابتة العرض فلا تهتز ساعة MTTD، ومعرّفات `INC-####` وعناوين IP وأوامر المصنّع واضحة وقابلة للنسخ |

الترخيص: كلاهما SIL Open Font License 1.1 (استخدام تجاري مسموح، مع تضمين الخط في الحزمة).

### 4.1 السلّم

| التوكن | الحجم | الوزن | الاستخدام |
|---|---|---|---|
| `--fs-2xs` | 11px | 400 | تسميات الخط الزمني |
| `--fs-xs` | 12px | 500 | رؤوس الجداول، الشارات، `kbd` |
| `--fs-sm` | 13px | 400 | الجداول الكثيفة، صفوف الأدلة |
| `--fs-base` | 14px | 400 | نص الواجهة الافتراضي |
| `--fs-md` | 16px | 400/500 | نص الشرح (Explanation)، اسم السبب الجذري |
| `--fs-lg` | 20px | 600 | عناوين اللوحات |
| `--fs-xl` | 24px | 600 | عنوان الصفحة |
| `--fs-2xl` | 32px | 600 | عناوين الحالات الفارغة، أرقام لوحة Alert Storm |
| `--fs-3xl` | 48px | mono 500 | أرقام KPI في Analytics |
| ساعة MTTD | 52px (Presenter: 72px) | mono 500 | `.rq-stopwatch` |

### 4.2 قواعد العربية

- ارتفاع السطر **1.75** للعربية و**1.5** للاتينية (مطبّق تلقائيًا عبر `html[lang]`).
- **لا تباعد حروف في العربية أبدًا** (يقطع اتصال الحروف). التباين −1% للعناوين اللاتينية فقط.
- **لا حروف كبيرة (ALL CAPS) كتسميات.** غيّروا `SIMULATION` و`LIVE LAB` في الشريط العلوي إلى «Simulation» و«Live lab» (والعربية «محاكاة» و«مختبر حي»).
- **أرقام لاتينية في الواجهة العربية** (لأن البيانات تقنية ومتطابقة مع المصنّعين). للتنسيق: `new Intl.NumberFormat("ar-SA-u-nu-latn")`. للنسبة اكتب الرقم ثم `%` يدويًا، لأن `style: "percent"` يعطي `٪` العربية.
- أي نص لاتيني أو رقم بوحدة داخل جملة عربية يُعزل: `<bdi>94.2%</bdi>` أو في CSS `direction: ltr; unicode-bidi: isolate` (الأوامر والمعرّفات والـ IP دائمًا).

---

## 5. الشكل والمسافات والعمق

| | القيمة |
|---|---|
| وحدة المسافة | 4px: `--sp-1…14` = 4, 8, 12, 16, 20, 24, 32, 40, 56 |
| الزوايا (أربعة مستويات حسب الدور) | `--r-sm` 6 حقول وخلايا · `--r-md` 10 أزرار وبطاقات داخل لوحة · `--r-lg` 16 لوحات عائمة · `--r-pill` الشارات والمفاتيح |
| الحدود | `--border-subtle` فواصل الجداول · `--border` حدود اللوحات والحقول · `--border-strong` hover |
| العمق | في الداكن: **حد + لون سطح**، لا ظل. الظل (`--shadow-float`) للوحات العائمة فقط |
| الإطار | الشريط الجانبي 72px · الشريط العلوي 56px · الخط الزمني 72px · لوحة الحادثة 420px |
| الخريطة | `--bg-canvas` مع شبكة نقاط 24px بشفافية 7% (`--topo-grid`) |
| الكثافة | صف الجدول 40px (30px للمدمج) · حقل 36px · زر 36px / 30px |
| الاتجاه | خصائص منطقية دائمًا: `margin-inline-start`, `inset-inline-end`, `text-align: start`. الخريطة وحدها **لا تنعكس** في RTL |

---

## 6. الحركة

القاعدة: لا حركة تلقائية في التطبيق إلا اثنتين. كل ما عداهما يستجيب لفعل المستخدم فقط.

| الحركة | متى | المواصفات |
|---|---|---|
| **التقارب** (حركة العلامة) | مرة واحدة عند ظهور السبب الجذري | شارات التنبيهات الخام تنزلق نحو عدّاد «1 حادثة» (`rq-converge`، 640ms، `--ease-in-out`)، ثم تنبض الحلقة مرة واحدة (`rq-halo`، 900ms) |
| **نبض Live lab** | مستمر على شارة الوضع فقط | `rq-live-pulse` 2.4s |

- المدد: `--dur-fast` 120ms (hover) · `--dur` 200ms (فتح/طي) · `--dur-slow` 360ms.
- ساعة MTTD والعدّادات: **بلا تحريك أرقام (tweening)**؛ تتحدث مباشرة.
- لا انزلاق/ظهور لأقسام الصفحة عند التحميل، ولا hover متحرك على كل بطاقة.
- `prefers-reduced-motion` مُحترم في `tokens.css` (كل الحركات تُلغى).

```tsx
// مثال التقارب: لكل شارة تنبيه (dx, dy) = متجه من الشارة إلى عدّاد الحادثة
chip.style.setProperty("--dx", `${dx}px`);
chip.style.setProperty("--dy", `${dy}px`);
chip.style.animation = "rq-converge var(--dur-converge) var(--ease-in-out) forwards";
halo.style.animation = "rq-halo 900ms var(--ease-out) 1";
```

---

## 7. المكوّنات

| المكوّن | المواصفات |
|---|---|
| **زر أساسي** | `--brand` خلفية، `--text-on-brand` نص، ارتفاع 36، `--r-md`. الاستخدام: «اعتماد المعالجة» وحده في الشاشة |
| **زر ثانوي** | `--bg-raised` + `--border`. **زر هادئ**: شفاف، hover `--bg-hover` (إقرار، إعادة ضبط) |
| **شارة حالة (chip)** | شكل حبّة `--r-pill`، خلفية `--x-soft`، نص `--x`، **شكل + نص** (● ▲ ◆) |
| **شارة الوضع** | Simulation: حد **منقّط** `--mode-sim` (غير حقيقي). Live lab: حد **متصل** `--mode-live` + خلفية `--brand-soft` + نبض |
| **عنصر التنقل** | أيقونة 20px داخل 44px. النشط: `--bg-selected` + خط 3px بلون `--brand` على حافة البداية |
| **جدول** | رأس `--fs-xs` 500 `--text-2`، صفوف 40px، فاصل `--border-subtle` سفلي فقط، hover `--bg-hover`، الأرقام والمعرّفات mono |
| **لوحة عائمة** | `--bg-float` + blur 14px + `--r-lg` + `--shadow-float` |
| **حلقة الثقة** | قطر 72، سماكة 6، التقدّم `--brand` بأطراف دائرية، الرقم mono في الوسط |
| **شريط المراحل** | 6 مقاطع بارتفاع 4px؛ المنجَز والحالي `--brand`، الحالي بهالة `--brand-soft` |
| **علامات الخط الزمني** | أشكال 18px: ▲ حقن `--warn` · ● أول شذوذ `--text-2` · ◆ سبب جذري `--crit` · ✓ موافقة `--brand` · ★ تعافٍ `--ok` (✕ رفض `--crit`، ⚙ تنفيذ `--text-2`) |
| **مفتاح الوكيل** | pill؛ المفعّل `--brand`. الوكلاء الأساسية المقفلة: أيقونة قفل + `aria-disabled="true"` |
| **الرسوم البيانية** | أعمدة `--chart-1`، خط الهدف 60s متقطع `--chart-ref` مع تسمية «Target 60s» |
| **تركيز لوحة المفاتيح** | `outline: 2px solid var(--focus-ring); outline-offset: 2px` على كل عنصر تفاعلي |
| **الأيقونات** | خطية، سماكة 1.75، 20px، أطراف ووصلات دائرية. ابقَ على مكتبتك الحالية واضبط `strokeWidth` و`size` فقط (انظر `preview.html` كمرجع للأشكال) |

---

## 8. الصفحات الثماني: ماذا يتغيّر في كل صفحة

**الإطار المشترك** — `frontend/src/components/layout/`
شريط جانبي 72px بخلفية `--bg-panel`؛ استبدل نص `RQ` بـ `<RootIQMark size={40} />`. الشريط العلوي: «RootIQ» ثم اسم الصفحة بـ `--text-3`، شارة الوضع الجديدة، نقطة الاتصال (● `--ok`)، «آخر تحديث» بخط mono. شريط **Reconnecting** بـ `--crit-soft` وحد `--crit` مع أيقونة. الخط الزمني بالأشكال أعلاه.

**Operations `/`** — `pages/OperationsPage.tsx`، `components/topology/`، `components/demo/`
الخريطة على `--bg-canvas` بشبكة نقاط. السبب الجذري: الرابط/الجهاز بـ `--topo-root` وسماكة 4 مع **عقدة + حلقة** (نفس لغة الشعار)؛ مسار التأثر بـ `--topo-affected` متقطع. Alert Storm: الرقم القديم (74) `--text-3` مشطوب، الرقم الجديد (1) `--brand-text`، شارة تقليل الضجيج `ok`. ساعة MTTD mono بلون `--ok` ثم `--warn` حسب الهدف. أزرار Demo ثانوية مع `kbd` للاختصار. شارة «كل شيء سليم»: chip `ok`.

**Incidents `/incidents`**
مرشحات الحالة كشريط مقاطع (segmented): العنصر المحدد `--bg-selected` + `--brand-text`. الشدة chip بشكل + لون. معرّف `INC-####` mono.

**Devices `/devices`**
حقل بحث 36px بأيقونة. حالة الجهاز chip من حقل الحالة نفسه (لا تضف عتبات ألوان جديدة في الواجهة). IP وCPU وعدد المنافذ mono.

**Services `/services`** (حالة فارغة)
بدلاً من `Services — Coming soon`: أيقونة العقدة والحلقة بحجم 48 بـ `--text-3`، عنوان `--fs-xl`، وسطر: «حالة الخدمات الحية تظهر الآن في Operations وداخل كل حادثة.» مع زر ثانوي «فتح Operations».

**Agents `/agents`**
بطاقات الوكلاء الـ16 على شبكة 3 أعمدة، `--bg-panel` + `--border-subtle`. مستوى الاستقلالية chip نصي. مخطط التدفق: المرحلة النشطة `--brand`، المنتهية `--ok`. Trace: جدول mono. Copilot: فقاعة المستخدم `--bg-raised`، فقاعة الرد `--bg-panel` بحد، وchip «للقراءة فقط» (`info`) ثابت أعلى اللوحة.

**Analytics `/analytics`**
أربع بطاقات KPI: التسمية `--text-2` xs، الرقم mono 48px. أعمدة `--chart-1` وخط 60s `--chart-ref`. عمود Correct بالأشكال ✓/✕ مع `--ok`/`--crit`.

**Audit `/audit`**
Time وTarget mono. عمود Action كـ chip: `approve` ok · `reject` warn · `guardrail_denied` crit · `toggle` info.

**Settings `/settings`**
إضافة قسمين لقسم Engineer name الموجود: **المظهر** (داكن/فاتح) و**اللغة**. المفتاح المحفوظ `rootiq.theme` بنفس نمط `rootiq.engineer`.

**لوحة الحادثة** — `components/incidents/`
بالترتيب نفسه في `UI.md §8` (رأس + مراحل، سبب جذري بحلقة الثقة، Why، Explanation، Replay، Evidence، Affected services، Action card، Recovery، Similar، Acknowledge). بطاقة الإجراء على `--bg-raised` بحد؛ **«اعتماد المعالجة» الزر الأساسي الوحيد في اللوحة**، و«رفض» ثانوي، وتحته سطر `--text-3`: «لا يُنفَّذ أي تغيير دون موافقة مهندس.»

---

## 9. الصوت والنصوص

- جمل قصيرة، أفعال مباشرة، نبرة هادئة. لا مبالغة ولا «سحر الذكاء الاصطناعي». اذكر المصدر ودرجة اليقين (template / LLM grounded) كما هو الآن.
- الزر يقول ما سيحدث، ويحمل الاسم نفسه في كل مكان في الرحلة (الزر «اعتماد المعالجة» → رسالة «اعتُمدت المعالجة»).
- الخطأ يقول ما حدث وماذا تفعل، ولا يعتذر.

| EN | AR |
|---|---|
| Approve remediation | اعتماد المعالجة |
| Reject | رفض |
| Acknowledge | إقرار |
| Root cause | السبب الجذري |
| Alert storm | عاصفة التنبيهات |
| Affected services | الخدمات المتأثرة |
| Recommended action | الإجراء المقترح |
| Simulation / Live lab | محاكاة / مختبر حي |
| Time to root cause | الزمن حتى السبب الجذري |

| الموقف | EN | AR |
|---|---|---|
| انقطاع WebSocket | Connection to the server was lost. Retrying automatically. | انقطع الاتصال بالخادم. نعيد المحاولة تلقائيًا. |
| Analytics بلا تشغيلات | No runs yet. Complete one demo loop and results will appear here. | لا توجد تشغيلات بعد. أكمل دورة عرض واحدة لتظهر النتائج هنا. |
| ثقة منخفضة | Low confidence. More investigation is needed before acting. | الثقة منخفضة. يلزم مزيد من التحقق قبل التنفيذ. |
| رفض من الخادم (403) | Only a named engineer can approve changes. | الاعتماد متاح لمهندس مسمّى فقط. |

---

## 10. خطة التنفيذ (4 أيام)

كل الأوامر من جذر المستودع. غيّر `BRAND` إلى مكان فك ضغط الحزمة.

### اليوم 1 — الأساس: التوكنز والخطوط والشعار

```bash
export BRAND=~/Downloads/rootiq-brand
cd frontend
mkdir -p src/styles src/components/brand public/brand scripts
cp $BRAND/tokens.css           src/styles/tokens.css
cp $BRAND/Logo.tsx             src/components/brand/Logo.tsx
cp $BRAND/logo/*.svg           public/brand/
cp $BRAND/logo/favicon.svg     public/favicon.svg
cp $BRAND/check-contrast.mjs   scripts/check-contrast.mjs
npm i @fontsource-variable/readex-pro @fontsource/ibm-plex-mono
```

أضف في `frontend/src/main.tsx` في **أعلى** الاستيرادات:

```ts
import "@fontsource-variable/readex-pro";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "@fontsource/ibm-plex-mono/600.css";
import "./styles/tokens.css";
```

في `frontend/index.html` اجعل الوسم الأول والعنوان هكذا:

```html
<html lang="ar" dir="rtl" data-theme="dark">
  <head>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="theme-color" content="#0C1030" />
```

أنشئ `frontend/src/lib/theme.ts` واستدعِ `initAppearance()` في `main.tsx` قبل `createRoot(...)`:

```ts
export type Theme = "dark" | "light";
export type Lang = "ar" | "en";
const THEME_KEY = "rootiq.theme";

export function setTheme(t: Theme) {
  localStorage.setItem(THEME_KEY, t);
  document.documentElement.dataset.theme = t;
}
export function applyLang(l: Lang) {
  document.documentElement.lang = l;
  document.documentElement.dir = l === "ar" ? "rtl" : "ltr";
}
export function initAppearance(lang: Lang = "ar") {
  document.documentElement.dataset.theme = (localStorage.getItem(THEME_KEY) as Theme) || "dark";
  applyLang(lang);
}
```

ابحث عن زر `ع / EN` واستدعِ `applyLang(...)` عند التبديل:

```bash
grep -rn "ع / EN\|setLang\|i18n" src | head
```

أضف في `package.json` ضمن `scripts`: `"check:contrast": "node scripts/check-contrast.mjs src/styles/tokens.css"`.

**معايير القبول (اليوم 1):**
1. `npm run check:contrast` ينتهي بـ `All contrast checks passed` ورمز خروج 0 (`echo $?` يطبع 0).
2. `npm run dev` ثم في الـ Console:
   `getComputedStyle(document.documentElement).getPropertyValue("--signal-400").trim()` يعيد `#3DD6F5`.
   `getComputedStyle(document.body).fontFamily` يبدأ بـ `"Readex Pro Variable"`.
3. تبويب Network → Font يُظهر `readex-pro-arabic-wght-normal.woff2` و`ibm-plex-mono-latin-400-normal.woff2`.
4. أيقونة التبويب هي favicon الجديد، و`<html>` يحمل `lang="ar" dir="rtl" data-theme="dark"`.

### اليوم 2 — استبدال كل الألوان

**1) جرد الألوان الحالية:**

```bash
cd frontend
grep -rhoE "#[0-9a-fA-F]{3,8}\b" src --include=*.tsx --include=*.ts --include=*.css \
  | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -40
grep -rnE "#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(" src --include=*.tsx --include=*.ts --include=*.css \
  | grep -v "src/styles/tokens.css" > /tmp/color-audit.txt
wc -l /tmp/color-audit.txt
```

**2) اربط كل لون قديم بدوره:** خلفية التطبيق → `--bg-app` · اللوحات → `--bg-panel` · نص أساسي/ثانوي → `--text-1`/`--text-2` · أخضر → `--ok` · أصفر/برتقالي → `--warn` · أحمر → `--crit` · أزرق/لون العلامة → `--brand`.

**3) الاستخدام:**

```css
/* CSS / CSS Modules */
.panel { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: var(--r-md); }
```

إن كان المشروع Tailwind v3 (`ls tailwind.config.*`) أضف ضمن `theme.extend`:

```js
colors: {
  canvas: "var(--bg-canvas)", app: "var(--bg-app)", panel: "var(--bg-panel)", raised: "var(--bg-raised)",
  fg: "var(--text-1)", "fg-2": "var(--text-2)", "fg-3": "var(--text-3)",
  brand: "var(--brand)", ok: "var(--ok)", warn: "var(--warn)", crit: "var(--crit)",
},
fontFamily: { sans: ["var(--font-ui)"], mono: ["var(--font-mono)"] },
borderRadius: { sm: "var(--r-sm)", md: "var(--r-md)", lg: "var(--r-lg)" },
```

**4) الخريطة (إن كانت `<canvas>`):** لا تضع hex داخل الرسم. اقرأ التوكنز وقت التشغيل وأعد الرسم عند تغيّر الثيم:

```ts
const css = getComputedStyle(document.documentElement);
const token = (n: string) => css.getPropertyValue(n).trim();
ctx.strokeStyle = token("--topo-root");
new MutationObserver(redraw).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
```

(أعد استدعاء `getComputedStyle` داخل `redraw` حتى تقرأ القيم الجديدة.)

**معايير القبول (اليوم 2):**
1. هذا الأمر يطبع `0`:
   ```bash
   grep -rnE "#[0-9a-fA-F]{3,8}\b" src --include=*.tsx --include=*.ts --include=*.css | grep -v "src/styles/tokens.css" | wc -l
   ```
   (أي استثناء يُوثَّق بتعليق يشرح السبب.)
2. اكتب في الـ Console `document.documentElement.dataset.theme = "light"`: كل الصفحات تتحول للفاتح دون عنصر واحد بقي بلون الداكن (خلفية سوداء، نص غير مقروء).
3. على الخريطة: السبب الجذري أحمر بحلقة، مسار التأثر كهرماني متقطع، والباقي محايد.

### اليوم 3 — الإطار والصفحات

بالترتيب، وبعد كل بند شغّل `npm run dev` وقارن بـ `preview.html`:

1. **الإطار:** `src/components/layout/Shell.tsx` وملفات Sidebar/TopBar بجانبه. استبدل `RQ` بـ:
   ```tsx
   import { RootIQMark } from "../brand/Logo";
   <RootIQMark size={40} />
   ```
   اجعل عرض الشريط الجانبي `var(--rail-w)` والشريط العلوي `var(--topbar-h)` والخط الزمني `var(--timeline-h)`.
2. **شارة الوضع:** في TopBar غيّر نص `SIMULATION` / `LIVE LAB` إلى «Simulation» / «Live lab» وطبّق نمط `.mode--sim` (حد منقّط) و`.mode--live` (حد متصل + `rq-live-pulse`) كما في `preview.html`.
3. **Presenter:** في `src/hooks/useHotkeys.ts` ابحث عن `Shift+P` (`grep -n -i "presenter" src/hooks/useHotkeys.ts`) وأضف عند التفعيل/الإلغاء:
   ```ts
   document.documentElement.dataset.presenter = on ? "on" : "off";
   ```
4. **Operations** ثم **لوحة الحادثة** ثم **Agents** ثم **Incidents / Devices / Analytics / Audit / Settings / Services** حسب §8.
5. **Settings:** أضف خيار المظهر مستدعيًا `setTheme("dark" | "light")` من `lib/theme.ts`.
6. **النصوص:** طبّق جدول §9 على الأزرار والرسائل الموجودة (`grep -rn "Approve Remediation\|Coming soon\|Reconnecting" src`).

**معايير القبول (اليوم 3):**
1. السايدبار 72px: `document.querySelector("nav").getBoundingClientRect().width` يعيد `72` (عدّل المحدد إن كان الوسم غير `nav`).
2. لوحة الحادثة 420px، وفي الشاشة كلها **زر أساسي واحد** («اعتماد المعالجة») عند ظهور بطاقة الإجراء.
3. `Shift+P` يخفي السايدبار ويكبّر الخطوط، وساعة MTTD تصبح 72px.
4. لا يوجد نص حروف كبيرة كتسمية (`grep -rn "uppercase" src` لا يعيد إلا ما له سبب موثّق).
5. صفحة Services لا تعرض `Coming soon` بل الحالة الفارغة المعرّفة.

### اليوم 4 — RTL وإمكانية الوصول والمراجعة

**1) الخصائص الفيزيائية → منطقية:**

```bash
cd frontend
grep -rnE "margin-(left|right)|padding-(left|right)|\b(left|right) *:|text-align: *(left|right)|border-(left|right)" src --include=*.css --include=*.tsx
# Tailwind: ml- mr- pl- pr- left- right- text-left text-right  →  ms- me- ps- pe- start- end- text-start text-end
grep -rnE "\b(ml|mr|pl|pr)-[0-9]|\b(left|right)-[0-9]|text-(left|right)" src --include=*.tsx
```

حوّلها إلى `margin-inline-start/end` و`padding-inline-*` و`inset-inline-*` و`text-align: start/end`.

**2) تحقق آلي:**

```bash
npm run check:contrast
npx lighthouse http://localhost:5173 --only-categories=accessibility --chrome-flags="--headless" --quiet --output=json --output-path=/tmp/lh.json
node -e "console.log(Math.round(require('/tmp/lh.json').categories.accessibility.score*100))"
```

**3) يدوي:** تنقّل كامل بـ `Tab` (كل عنصر تفاعلي له حلقة تركيز واضحة)، وفعّل «تقليل الحركة» في النظام وتأكد أن «التقارب» و«النبض» توقفا.

**معايير القبول (اليوم 4):**
1. أمر البحث في الخطوة 1 لا يعيد إلا الخريطة (canvas) وملفات `tokens.css`.
2. في RTL: الشريط الجانبي على اليمين، لوحة الحادثة على اليسار، لا شريط تمرير أفقي في أي صفحة من الثماني عند عرض 1280px.
3. `npm run check:contrast` ينجح، ودرجة Lighthouse لإمكانية الوصول ≥ 95 (هدف، وأي بند فاشل يُصلَح أو يُوثَّق).
4. كل chip حالة يُقرأ بدون لون: الشكل والنص ظاهران (جرّب `filter: grayscale(1)` على `<html>` من أدوات المطور).
5. لقطة Operations (داكن/عربي) تطابق `preview.html?theme=dark&lang=ar` في: العرض 72/56/420، الألوان، الخط، موضع الحلقة على السبب الجذري.

---

## 11. قائمة القبول النهائية

- [ ] `check:contrast` ناجح للوضعين
- [ ] صفر hex خارج `tokens.css` (أو استثناءات موثّقة)
- [ ] الخطان يُحمَّلان من الحزمة (بدون طلبات لخوادم خارجية)
- [ ] الشعار: السايدبار، favicon، صفحة الدخول إن وُجدت، وملف `rootiq-app-icon.svg` في manifest إن كان PWA
- [ ] داكن وفاتح وعربي وإنجليزي يعملان على الصفحات الثماني
- [ ] حركتان تلقائيتان فقط (التقارب، نبض Live lab)
- [ ] `Shift+P` وPresenter سليمان
- [ ] لا نص بحروف كبيرة، ولا تباعد حروف في العربية

---

## 12. ما تحققتُ منه وما لم أتحقق منه

**تحققتُ:** رسمتُ كل ملفات الشعار وراجعتُها بصريًا على الخلفيتين وبأحجام 16/32/48؛ شغّلتُ `preview.html` في متصفح حقيقي بالوضع الداكن/العربي والفاتح/الإنجليزي وأصلحتُ مشاكل الاتجاه التي ظهرت؛ شغّلتُ `check-contrast.mjs` على `tokens.css` الفعلي ونجحت كل الفحوص؛ تأكدتُ من أسماء حزم الخطوط وإصداراتها (5.3.0) في سجل npm، ومن أن اسم العائلة `Readex Pro Variable` يطابق ما في `tokens.css`.

**لم أتحقق:** تشغيل هذه الخطوات على كود `frontend/` الحقيقي (لم يصلني)؛ أسماء المحددات في أوامر القبول (مثل `nav`) قد تحتاج تعديلًا؛ درجة Lighthouse؛ وأي مكتبة أيقونات تستخدمونها. وصفحة المعاينة مفحوصة على Chromium فقط.
