# Changelog — branch `my-edits`

Everything below is on top of the team's `main` (`db7913c`). Newest first. Each entry says **what changed, why, and what was verified**.
(الفرع `my-edits` فقط؛ لا شيء هنا على `main`.)

## Fix: cell E1 on Colab (found when exporting the merged model)
- Colab ships `torchao` 0.10.0, and the newest `peft` raises "Found an incompatible version of torchao ... only versions above 0.16.0 are supported" when the adapter is loaded. E1 now removes an old `torchao` first (the notebook does not use it; the 4-bit weights come from bitsandbytes). In a local environment it stops with the exact command to run instead of changing the user's packages.
- E1 used `del trainer, tuned, model` first, so after a failed attempt it could not be rerun (NameError). It now frees the GPU tolerantly, so the cell can be rerun.
- `torch_dtype` (deprecated) is replaced by `dtype` on transformers 4.56 or newer.
- Verified: 2 new tests run E1 with stand-ins (old torchao removed, compatible torchao left alone, local run refuses to modify packages, rerun after a failure, `dtype` name by version); 266 backend tests pass. The real merge and save on a GPU is still verified only by the Colab run.

## Wiring audit in CI (`scripts/audit_wiring.py`)
- Starts the real API on the multi-vendor example topology and checks: 16 agents in the roster and the flow, 43 vendors, the five lab vendors identified with their config model, `sysDescr` identification (FortiOS, Junos, EOS, AOS-CX on two models, ArubaOS-Switch), syslog normalization with the knowledge base's own example lines, the Cisco/Arista shared format (Cisco chosen and Arista listed in `alsoMatches` without a device, Arista when the line is sent for the Arista switch), unknown lines counted as unparsed, and the Copilot save-config answer in English and Arabic.
- Also checks that the test count, agent count and vendor count stated in README and the prompts match the code, that relative markdown links resolve, that the notebook clones the fork and has the fixed C2, that the workflows and custom agents parse, and that the frontend types carry `vendorContext` and `configModel`.
- Added as a step of the `consistency` CI job. Vendor data reaches the UI through the incident plan (`vendorContext`, `plan.vendorCommands`), not through `/api/vendors`, which is for API users.
- Verified locally: 36 checks pass; frontend `tsc`, `vitest` (3 tests) and the production build pass.

## Fix: cell C2 on the newest TRL / transformers (found in the first real Colab run)
- Colab installs the newest `transformers` / `trl`, which no longer accept `warmup_ratio`. C2 now passes `warmup_steps` (3% of the planned steps, as a whole number that old and new versions accept).
- The blind `max_length` / `max_seq_length` retry hid that error behind a second one. C2 now looks at the fields of the installed `SFTConfig` and picks `max_length` vs `max_seq_length` and `eval_strategy` vs `evaluation_strategy`, picks `processing_class` vs `tokenizer` for `SFTTrainer` from its signature, and stops with a message that names any argument the installed version does not know.
- Verified: 2 new tests run C2 against stand-ins for an older and a newer release (smoke and full); 264 backend tests pass. C1 to E1 on a real GPU are still verified only by the Colab run.

## Prompt 3: GitHub Agents tab check
- `docs/GITHUB_AGENTS_PROMPT.md`: a read-only Claude in Chrome prompt that checks the workflows, the Agents tab, the two custom agents and the Copilot plan, and starts one test session only after `go test`.

## Old-vs-new safeguards for Colab and Drive
- C2 refuses to train on a `train.jsonl` left on Drive by an old run (it must contain vendor-knowledge rows and `kb_test_seen.jsonl` must exist), and the checkpoint folder name ends with a hash of the training data.
- The Colab operator prompt says to open the notebook only from GitHub and to stop on any copy that does not print `commit: <hash>` in cell 3.

## Notebook fixes found in review (before the first GPU run)
- C2: the SMOKE run and the full run no longer share a checkpoint folder (the full run would have resumed from the 20-step smoke checkpoint with a finished learning-rate schedule); the adapter and the merged model carry the same `-smoke` suffix.
- C2: `per_device_eval_batch_size=2` (the default of 8 with a 152k-token vocabulary can exhaust a T4) and `padding_side = "right"` for training (batched decoding in C1 sets it to left).
- Not run on a GPU: these are fixes from code review, verified only by the notebook tests (cells compile, CPU cells run).

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

## Priority vendors: Juniper, Fortinet, Aruba, Arista (+ the Cisco lab)
Why: field engineers pointed at the two real differences between vendors — how commands are written and how a change is saved (NVRAM / commit) — and the virtual lab is Cisco.
- **Config model per OS** (`running-startup` / `candidate-commit` / `auto-save` with enter, save, restore point, safe change, rollback) and **CLI style** (EN/AR) for Cisco (IOS-XE, IOS, NX-OS, IOS-XR), Junos, EOS, AOS-CX, ArubaOS-Switch, FortiOS, FortiSwitchOS, RouterOS, VRP, OS10, EXOS, Cumulus.
- Fortinet: separate FortiOS command table, more FortiSwitchOS commands, FortiGate identity, interface-status syslog pattern. Aruba: ArubaOS-Switch link events. Config-change syslog (`%SYS-5-CONFIG_I`, `UI_COMMIT`). Virtual-lab names (`vQFX`, `vEOS`, `FortiGate-VM`, `AOS-CX`).
- `vendorContext.devices[].configModel` and `plan.vendorCommands.devices[].configModel`; UI block "Applying a change"; Copilot answers save/commit/rollback/CLI-style questions for up to 4 vendors side by side.
- `configs/topology.multivendor.example.json` (Cisco + Juniper vQFX + Arista vEOS + FortiGate-VM + Aruba AOS-CX).
- Training: new `config_model` task (10 tasks, 4,728 examples); cross-vendor command pairs start with these five vendors; notebook ship rule also checks `config_model`.
- Retrieval: short threshold facts win ties against long docs.
- Verified: 262 backend tests (new `test_multivendor.py`), `tsc`, vitest, Vite build, and a real browser check of the plan UI.

## Multi-vendor knowledge base, `vendor` + `logs` agents, `training/`
- **Knowledge base** (`backend/app/knowledge/`): 43 vendors, 59 OS families, 103 device series, 25 problem patterns, 26 capabilities as JSON; identify from `sysObjectID` / `sysDescr` / hint, version normalization, per-OS command tables (`default_for`), syslog parsing, EN/AR problem matching, and a `validate()` that rejects change verbs in read-only lists, duplicate enterprise numbers, bad regexes and examples that do not match their own regex.
- **Agents 14 → 16:** `vendor` (device identity, matched problems, per-vendor read-only diagnostics) and `logs` (multi-vendor syslog → `syslog_link_down` events on the topology link). Modified: topology, knowledge/RAG, Copilot (`vendor_help`), remediation (`plan.vendorCommands`), guardrail (`vendor_commands_read_only`), orchestrator (`vendor.enrich`).
- **API:** `/api/vendors`, `/api/vendors/{id}`, `/api/vendors/inventory`, `POST /api/vendors/identify`, `/api/problems[/{id}]`, `POST /api/syslog`, `/api/syslog/recent`.
- **Training folder** (`training/`): deterministic dataset builder (train / val / test_seen / test_unseen + manifest), offline scorer (invented / unsafe command rates), Hugging Face catalog with licences and use policy, licence-gated external loader, Colab notebook (stages A–E) and the Colab operator prompt.
- **LLM:** `LLM_PROVIDER=custom` (any OpenAI-compatible server) for your own fine-tuned model.
- Verified: 248 backend tests, notebook CPU cells executed in a test, ship-decision logic exercised with stand-ins, live HTTP check of the new endpoints.
- Not verified: GPU cells (C1, C2, D1, E1) — PyTorch is blocked on the development machine.

## Live-run fixes
- Analysis is no longer cancelled by every new symptom (root cause had appeared only after ~80 s with a slow LLM); regression test added.
- Copilot LLM hardening: refusal and "dropped headline percentage" answers are rejected; fixed messages are never sent to the model; 429 cooldown honouring `Retry-After`; usage counters; Groq default model updated.
- Incident ids continue after a restart; verification grace window (`VERIFY_GRACE_S`); `scripts/run-demo.ps1`.
- Verified with a real Groq key (explanations and Copilot answers with grounded numbers), Playwright ×3 in a real browser, and live-mode contract tests.

## Multi-agent layer
- 14 agents (orchestrator, telemetry, detection, topology, correlation, RCA, explanation, knowledge/RAG, Copilot, remediation, guardrail, execution, verification, learning) with per-agent timeouts, deterministic fallbacks, kill switches and a trace store (`agent_step` WebSocket event).
- Fail-closed Guardrail (human-only approval, whitelist, state, rate limit, lab isolation), playbooks with rollback and numeric verification criteria, postmortems fed back into the index, local TF-IDF RAG with secret redaction and prompt-injection filtering, bilingual read-only Copilot.
- UI: Agents page (roster, flow, live trace, Copilot), plan details, recovery verification.
