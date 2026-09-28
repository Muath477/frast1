# Judge Q&A bank

Short answers for the pitch. Pair with `docs/ARCHITECTURE.md` and `docs/RESULTS.md`.

| Question | Answer |
|---|---|
| Is this real AI or just rules? | Hybrid on purpose: statistical baseline + optional multivariate Isolation Forest + graph reasoning + weighted ranking you can explain. Rules alone don’t generalize; pure ML needs labeled outages we don’t have — hybrid gives explainability, reliability, and a growth path. |
| How do you scale to thousands of devices? | Analysis runs on the **correlated symptom set**, not the whole fabric; graph path ops scale with the incident. Collectors are distributed and push a normalized schema. Auto-discovery via CDP/LLDP is in the Pilot roadmap. |
| What if RCA is wrong? | We show confidence, evidence, and candidates. If confidence &lt; 55% we say it needs investigation. **Nothing executes without human approval.** |
| Why not use an LLM for analysis? | LLM is for wording only and is grounded: any number not in measured evidence is rejected and we fall back to the template. Ranking itself is deterministic and auditable. |
| vs Datadog / Dynatrace / Splunk ITSI? | Vendor-neutral, light, hybrid + classic networks (SNMP/Syslog)—not cloud APM only—ties physical ports to services, with an approval loop built in. Private deploy fits data-sovereignty needs (e.g. KSA). |
| How do you learn over time? | Resolved, approved incidents bump `historical_support` for that root — confidence rises on later runs. Later: learn weights from closed incidents. |
| Security? | Read-only SNMP where possible, lab agent runs a **fixed whitelist** only, secrets in env, every decision in the audit log, full simulation mode. |
| Business model? | Subscription by monitored assets + enterprise integration + private deploy. First customers: enterprise NOCs, MSPs, DC/cloud ops. |
| What’s next? | Pilot with a real NOC: auto-discovery, broad SNMP, RBAC, ITSM hooks, then capacity foresight and change-impact analysis. |
| Is the data real or fake? | Live path uses a real EVE-NG lab (virtual Cisco + real iperf3). Sim mode is the backup and is **labeled on screen** when used. Measured numbers in `RESULTS.md` are from sim lab runs on this build (live lab fills the same table when available). |

## Who answers what

| Topic | Owner |
|---|---|
| Demo keyboard / UI | FE (Ahmed) |
| Ingest, actions, audit | BE |
| Ranking / evidence / LLM grounding | AI |
| EVE / collector / agent | INFRA |
| Story + business | Presenter |
