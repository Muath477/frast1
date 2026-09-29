# Changelog — branch `my-edits`

Everything below is on top of the team's `main` (`db7913c`). Newest first. Each entry says **what changed, why, and what was verified**.
(الفرع `my-edits` فقط؛ لا شيء هنا على `main`.)

## GitHub automation (CI, Copilot agent setup, custom agents)
- `.github/workflows/ci.yml`: backend pytest, frontend type-check + vitest + build, and a consistency job (knowledge base validates, generated training data and `docs/VENDORS.md` match the knowledge base).
- `.github/workflows/copilot-setup-steps.yml`, `.github/copilot-instructions.md`, `.github/agents/{vendor-kb,docs-keeper}.agent.md`: environment, rules and two custom agents for the Copilot coding agent (the Agents tab).
- `.github/pull_request_template.md`; `scripts/gen_vendors_doc.py` (generator of `docs/VENDORS.md`, with `--check`); a CI badge in the README.

## Agent prompts (VS Code and Colab + Drive + GitHub)
- `training/VSCODE_AGENT_PROMPT.md` (prompt 1): a coding agent inside VS Code trains locally: preflight of the machine, repo integrity, Stages A and B on the CPU, Stages C-E only when CUDA works with at least 8 GB of VRAM. It never commits or pushes, never touches `origin`, and works on a copy of the notebook.
- `training/COLAB_AGENT_PROMPT.md` (prompt 2): Claude in Chrome with three tabs (Colab, Google Drive read-only, GitHub read-only on the fork). It checks that the commit printed by the notebook equals the newest commit on GitHub and that the files the notebook reports are really on Drive.
- Notebook cell 3: clones branch `main` of the fork, prints the commit hash, and never runs `git pull` on a local checkout.

## Documentation refresh
- `README.md`: "What's new" table, 2-minute vendor demo (curl), explicit limits, tests and docs map; a note on switching the GitHub branch selector to `my-edits`.
- `CHANGELOG.md` (this file), `docs/README.md` index, `docs/DEMO_SCRIPT.md` (optional vendor segment), `docs/QA_BANK.md` (vendor questions).

## 897afad — Priority vendors: Juniper, Fortinet, Aruba, Arista (+ the Cisco lab)
Why: field engineers pointed at the two real differences between vendors — how commands are written and how a change is saved (NVRAM / commit) — and the virtual lab is Cisco.
- **Config model per OS** (`running-startup` / `candidate-commit` / `auto-save` with enter, save, restore point, safe change, rollback) and **CLI style** (EN/AR) for Cisco (IOS-XE, IOS, NX-OS, IOS-XR), Junos, EOS, AOS-CX, ArubaOS-Switch, FortiOS, FortiSwitchOS, RouterOS, VRP, OS10, EXOS, Cumulus.
- Fortinet: separate FortiOS command table, more FortiSwitchOS commands, FortiGate identity, interface-status syslog pattern. Aruba: ArubaOS-Switch link events. Config-change syslog (`%SYS-5-CONFIG_I`, `UI_COMMIT`). Virtual-lab names (`vQFX`, `vEOS`, `FortiGate-VM`, `AOS-CX`).
- `vendorContext.devices[].configModel` and `plan.vendorCommands.devices[].configModel`; UI block "Applying a change"; Copilot answers save/commit/rollback/CLI-style questions for up to 4 vendors side by side.
- `configs/topology.multivendor.example.json` (Cisco + Juniper vQFX + Arista vEOS + FortiGate-VM + Aruba AOS-CX).
- Training: new `config_model` task (10 tasks, 4,728 examples); cross-vendor command pairs start with these five vendors; notebook ship rule also checks `config_model`.
- Retrieval: short threshold facts win ties against long docs.
- Verified: 262 backend tests (new `test_multivendor.py`), `tsc`, vitest, Vite build, and a real browser check of the plan UI.

## 775b205 — Multi-vendor knowledge base, `vendor` + `logs` agents, `training/`
- **Knowledge base** (`backend/app/knowledge/`): 43 vendors, 59 OS families, 103 device series, 25 problem patterns, 26 capabilities as JSON; identify from `sysObjectID` / `sysDescr` / hint, version normalization, per-OS command tables (`default_for`), syslog parsing, EN/AR problem matching, and a `validate()` that rejects change verbs in read-only lists, duplicate enterprise numbers, bad regexes and examples that do not match their own regex.
- **Agents 14 → 16:** `vendor` (device identity, matched problems, per-vendor read-only diagnostics) and `logs` (multi-vendor syslog → `syslog_link_down` events on the topology link). Modified: topology, knowledge/RAG, Copilot (`vendor_help`), remediation (`plan.vendorCommands`), guardrail (`vendor_commands_read_only`), orchestrator (`vendor.enrich`).
- **API:** `/api/vendors`, `/api/vendors/{id}`, `/api/vendors/inventory`, `POST /api/vendors/identify`, `/api/problems[/{id}]`, `POST /api/syslog`, `/api/syslog/recent`.
- **Training folder** (`training/`): deterministic dataset builder (train / val / test_seen / test_unseen + manifest), offline scorer (invented / unsafe command rates), Hugging Face catalog with licences and use policy, licence-gated external loader, Colab notebook (stages A–E) and the Colab operator prompt.
- **LLM:** `LLM_PROVIDER=custom` (any OpenAI-compatible server) for your own fine-tuned model.
- Verified: 248 backend tests, notebook CPU cells executed in a test, ship-decision logic exercised with stand-ins, live HTTP check of the new endpoints.
- Not verified: GPU cells (C1, C2, D1, E1) — PyTorch is blocked on the development machine.

## d15bc18 — Live-run fixes
- Analysis is no longer cancelled by every new symptom (root cause had appeared only after ~80 s with a slow LLM); regression test added.
- Copilot LLM hardening: refusal and "dropped headline percentage" answers are rejected; fixed messages are never sent to the model; 429 cooldown honouring `Retry-After`; usage counters; Groq default model updated.
- Incident ids continue after a restart; verification grace window (`VERIFY_GRACE_S`); `scripts/run-demo.ps1`.
- Verified with a real Groq key (explanations and Copilot answers with grounded numbers), Playwright ×3 in a real browser, and live-mode contract tests.

## b62ae65 — Multi-agent layer
- 14 agents (orchestrator, telemetry, detection, topology, correlation, RCA, explanation, knowledge/RAG, Copilot, remediation, guardrail, execution, verification, learning) with per-agent timeouts, deterministic fallbacks, kill switches and a trace store (`agent_step` WebSocket event).
- Fail-closed Guardrail (human-only approval, whitelist, state, rate limit, lab isolation), playbooks with rollback and numeric verification criteria, postmortems fed back into the index, local TF-IDF RAG with secret redaction and prompt-injection filtering, bilingual read-only Copilot.
- UI: Agents page (roster, flow, live trace, Copilot), plan details, recovery verification.
