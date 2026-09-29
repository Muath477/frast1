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
| Is it really a multi-agent system? | Yes — 16 agents, each with one job, explicit inputs/outputs, limited tools and a traceable step (Agents page → Live trace). Fourteen are deterministic; only Explanation and the Copilot can use an LLM, optionally. |
| Can the AI act on its own? | No. Advisors only recommend. The Execution agent refuses without a named human approval **and** a fresh Guardrail verdict; `system` / `agent:*` approvals get HTTP 403 and are audited. |
| What if the LLM hallucinates? | Any number not present in the measured facts rejects the answer and we fall back to the template; Copilot answers must also cite sources. Everything works with the LLM off. |
| Can someone poison the docs to hijack the assistant? | Retrieved text is treated as data, injection-looking passages are excluded and flagged, and the Copilot has no tool that can approve, reject or execute. |
| Why 16 agents and not one big model? | Small units are testable, auditable and degrade independently (a slow LLM never blocks an incident); a single model would be a black box with execution risk. |
| How do the agents learn? | The Learning agent records confirmed root causes (raising confidence next time), writes a postmortem and feeds it back into the knowledge index. Weights and thresholds are never changed automatically. |

## Who answers what

| Topic | Owner |
|---|---|
| Demo keyboard / UI | FE (Ahmed) |
| Ingest, actions, audit | BE |
| Ranking / evidence / LLM grounding | AI |
| EVE / collector / agent | INFRA |
| Story + business | Presenter |
