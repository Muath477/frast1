"""The committed training data must be exactly what the knowledge base produces, leak-free, safe, and scoreable."""
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pytest

TRAINING = Path(__file__).resolve().parents[2] / "training"
sys.path.insert(0, str(TRAINING))

import build_dataset as bd  # noqa: E402
import kb_eval  # noqa: E402
from app.knowledge import get_kb  # noqa: E402

kb = get_kb()
GEN = TRAINING / "data" / "generated"


def load(split):
    return [json.loads(l) for l in (GEN / f"{split}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


@pytest.fixture(scope="module")
def built():
    return bd.build()


def test_committed_files_match_the_knowledge_base_and_the_generator(built):
    """If this fails: run `python training/build_dataset.py` and commit the regenerated files."""
    out, manifest = built
    committed = json.loads((GEN / "manifest.json").read_text(encoding="utf-8"))
    assert committed["kb_fingerprint"] == manifest["kb_fingerprint"], "knowledge base changed: regenerate the training data"
    for split in bd.SPLITS:
        text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out[split])
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == committed["files"][f"{split}.jsonl"], f"{split}.jsonl is stale"


def test_build_is_deterministic(built):
    _, m1 = built
    _, m2 = bd.build()
    assert m1["kb_fingerprint"] == m2["kb_fingerprint"] and m1["splits"] == m2["splits"]


def test_every_row_is_a_well_formed_chat_example():
    n = 0
    for split in bd.SPLITS:
        for r in load(split):
            n += 1
            roles = [m["role"] for m in r["messages"]]
            assert roles == ["system", "user", "assistant"], r["id"]
            assert all(m["content"].strip() for m in r["messages"])
            assert r["lang"] in ("en", "ar") and r["task"] and r["group"] and r["meta"]["gold"] is not None
            if r["lang"] == "ar":
                assert re.search(r"[؀-ۿ]", r["messages"][1]["content"]), r["id"]
    assert n > 3000


def test_no_secrets_or_personal_data_in_the_data():
    blob = "".join((GEN / f"{s}.jsonl").read_text(encoding="utf-8") for s in bd.SPLITS)
    for bad in (r"gsk_[A-Za-z0-9]{10,}", r"sk-[A-Za-z0-9]{20,}", r"(?i)password\s*[=:]", r"@gmail\.com", r"(?i)community\s+\w{4,}\s+ro"):
        assert not re.search(bad, blob), bad


def test_splits_do_not_leak():
    seen, group_split = {}, defaultdict(set)
    for split in bd.SPLITS:
        for r in load(split):
            key = (r["task"], r["messages"][1]["content"])
            assert key not in seen, f"same prompt in {seen[key]} and {split}"
            seen[key] = split
            group_split[r["group"]].add(split)
    unseen_groups = {g for g, s in group_split.items() if "test_unseen" in s}
    assert unseen_groups and all(group_split[g] == {"test_unseen"} for g in unseen_groups), "test_unseen groups must not appear in any other split"
    sizes = {s: len(load(s)) for s in bd.SPLITS}
    assert sizes["train"] > 8 * max(sizes["val"], sizes["test_seen"], sizes["test_unseen"]) * 0.9
    assert min(sizes.values()) >= 100


def test_identify_and_syslog_labels_are_exactly_what_the_kb_computes():
    checked = 0
    for split in bd.SPLITS:
        for r in load(split):
            user, gold = r["messages"][1]["content"], r["meta"]["gold"]
            if r["task"] in ("identify", "syslog"):
                assert json.loads(r["messages"][2]["content"]) == gold
            if r["task"] == "identify":
                body = user.split("\n", 1)[1]
                descr = re.search(r"^sysDescr: (.*?)(?:\nsysObjectID:|\Z)", body, re.S | re.M)
                oid = re.search(r"^sysObjectID: (\S+)", body, re.M)
                hint = re.search(r"^hint: (.*)$", body, re.M)
                got = kb.identify(descr.group(1) if descr else None, oid.group(1) if oid else None, hint.group(1) if hint else None)
                assert {k: got.get(k) for k in ("vendor", "os", "version", "model")} == gold, user
                checked += 1
            if r["task"] == "syslog":
                lines = user.split("\n")
                hint = next((l.split(": ", 1)[1] for l in lines if l.startswith(("Vendor hint:", "تلميح المصنّع:"))), None)
                line = lines[-1]
                parsed = kb.parse_syslog(line, hint)
                exp = {k: (parsed or {}).get(k) for k in ("event", "vendor", "interface", "state", "severity")}
                assert exp == gold, line
                checked += 1
    assert checked > 500


def test_every_vendor_is_identifiable_and_has_a_profile_in_the_data():
    rows = [r for s in bd.SPLITS for r in load(s)]
    for task in ("identify", "vendor_profile"):
        covered = {r["vendor"] for r in rows if r["task"] == task}
        assert set(kb.vendors) <= covered, f"{task}: missing {sorted(set(kb.vendors) - covered)}"


def test_commands_in_answers_are_read_only_or_kb_fix_commands():
    kn = kb_eval._Known(kb)
    for split in bd.SPLITS:
        for r in load(split):
            if r["task"] in ("safety_refusal",) or r["meta"]["gold"].get("abstain"):
                assert not kb_eval.command_candidates(r["messages"][2]["content"]), r["id"]
                continue
            for c in kb_eval.command_candidates(r["messages"][2]["content"]):
                assert kb.is_read_only(c) or (r["vendor"] and kn.is_kb_change(r["vendor"], c)), f"{r['task']}: {c}"
                if r["vendor"] and r["task"] in ("command_lookup", "command_translate", "problem_diagnose", "incident_vendor_plan"):
                    assert kn.known(r["vendor"], c), f"{r['task']} {r['vendor']}: command not in KB: {c}"


def test_abstention_examples_exist_and_never_contain_commands():
    ab = [r for s in bd.SPLITS for r in load(s) if r["meta"]["gold"].get("abstain")]
    assert len(ab) >= 60
    assert all(any(p in r["messages"][2]["content"].lower() for p in kb_eval.ABSTAIN_PHRASES) for r in ab)
    # ... and a vendor without a command table is only ever asked about, never answered with commands
    profile_only = {v for v, d in kb.vendors.items() if not d["commands"]}
    assert all(r["meta"]["gold"]["abstain"] for s in bd.SPLITS for r in load(s) if r["task"] == "command_lookup" and r["vendor"] in profile_only)


# ---------------------------------------------------------------- the scorer
def test_gold_answers_score_perfectly():
    rows = load("test_seen") + load("test_unseen")
    rep = kb_eval.evaluate(rows, lambda msgs: next(r["messages"][2]["content"] for r in rows if r["messages"][1]["content"] == msgs[1]["content"]))
    for t, e in rep["tasks"].items():
        assert e["accuracy"] == 1.0, (t, e)
    assert rep["invented_command_rate"] == 0.0 and rep["unsafe_command_count"] == 0


def test_garbage_scores_zero_and_invented_unsafe_commands_are_caught():
    rows = load("test_seen")
    bad = kb_eval.evaluate(rows, lambda msgs: "I think it is probably fine.")
    assert all(e["accuracy"] < 0.2 for t, e in bad["tasks"].items() if t not in ("safety_refusal",))
    cmd_row = next(r for r in rows if r["task"] == "command_lookup" and not r["meta"]["gold"]["abstain"])
    s = kb_eval.score_row(cmd_row, "Run `reload` and then `show fake-command-xyz` and `write erase`.")
    assert not s["ok"] and s["unsafe"] and s["invented"]


def test_abstain_rows_reward_saying_no_and_punish_inventing():
    row = next(r for s in bd.SPLITS for r in load(s) if r["meta"]["gold"].get("abstain") and r["lang"] == "en")
    assert kb_eval.score_row(row, row["messages"][2]["content"])["ok"]
    assert not kb_eval.score_row(row, "Use `show interfaces status`.")["ok"]


def test_refusal_rows_require_a_refusal_without_commands():
    row = next(r for s in bd.SPLITS for r in load(s) if r["task"] == "safety_refusal" and r["lang"] == "en")
    assert kb_eval.score_row(row, row["messages"][2]["content"])["ok"]
    assert not kb_eval.score_row(row, "Sure, running `reload` now.")["ok"]


def test_json_extraction_tolerates_prose_and_fences_and_normalizes_versions():
    assert kb_eval.extract_json('Here you go:\n```json\n{"vendor": "cisco", "os": null}\n```') == {"vendor": "cisco", "os": None}
    assert kb_eval.extract_json("no json here") is None
    row = next(r for s in bd.SPLITS for r in load(s) if r["task"] == "identify" and r["meta"]["gold"]["version"])
    pred = dict(row["meta"]["gold"])
    assert kb_eval.score_row(row, json.dumps(pred))["ok"]
    pred["vendor"] = "juniper" if pred["vendor"] != "juniper" else "cisco"
    assert not kb_eval.score_row(row, json.dumps(pred))["ok"]


# ---------------------------------------------------------------- optional external data
def test_external_loader_only_accepts_datasets_the_catalog_allows():
    import external

    assert external.allowed("zilalzihar/mikrotik-routeros-qa-dataset") and external.allowed("witfoo/syslog-to-artifact")
    for name in ("ndavidson/cisco_inam_chatml", "jack0503/junos_cli_qa", "Elfsong/Cisco_CCNA", "bolu61/loghub_2", "nobody/unknown"):
        assert not external.allowed(name)
        with pytest.raises(PermissionError):
            external.convert(name, [], 10)
        with pytest.raises(PermissionError):
            external.load_external(name)


def test_external_conversion_screens_secrets_size_duplicates_and_destructive_advice():
    import external

    name = "zilalzihar/mikrotik-routeros-qa-dataset"
    recs = [
        {"instruction": "How do I list interfaces?", "input": "", "output": "Use `/interface print`."},
        {"instruction": "How do I list interfaces?", "input": "", "output": "Use `/interface print`."},          # duplicate prompt
        {"instruction": "Set the admin login", "input": "", "output": "Set password = hunter2 and continue."},   # secret
        {"instruction": "Wipe it", "input": "", "output": "Run /system reset-configuration now."},              # destructive advice
        {"instruction": "x" * 2000, "input": "", "output": "too long prompt"},
        {"instruction": "Empty answer", "input": "", "output": ""},
        {"instruction": "Show routes", "input": "IPv4 only", "output": "`/ip route print`"},
    ]
    out = external.convert(name, recs, limit=10)
    assert sorted(r["messages"][1]["content"] for r in out) == ["How do I list interfaces?", "Show routes\nIPv4 only"]
    assert all(r["split"] == "train" and r["task"] == "ext_mikrotik_qa" and r["messages"][0]["content"] == external.SYSTEM for r in out)
    assert external.convert(name, recs, limit=1) == external.convert(name, recs, limit=1)  # deterministic
    art = external.convert("witfoo/syslog-to-artifact", [{"instruction": "Identify this syslog message", "input_text": "<134>x flows src=1.2.3.4", "output_text": "Product: Meraki | Vendor: Cisco"}], 5)
    assert art[0]["task"] == "ext_syslog_artifact"


# ---------------------------------------------------------------- the notebook's CPU-only cells still run
def _cells():
    nb = json.loads((TRAINING / "RootIQ_Training.ipynb").read_text(encoding="utf-8"))
    return nb, {("".join(c["source"]).split("\n")[0]): "".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"}


def _cell(cells, prefix):
    hits = [v for k, v in cells.items() if k.startswith(prefix)]
    assert len(hits) == 1, prefix
    return hits[0]


def test_notebook_defaults_are_safe_and_contain_no_secrets():
    nb, cells = _cells()
    setup = _cell(cells, "#@title 1)")
    assert re.search(r"^SMOKE = True", setup, re.M) and re.search(r"^INCLUDE_EXTERNAL = False", setup, re.M)
    text = json.dumps(nb)
    assert not re.search(r"gsk_[A-Za-z0-9]{10,}|sk-ant-|hf_[A-Za-z0-9]{20,}", text)
    assert all(not c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code"), "commit the notebook without outputs"
    titles = [k.split(")")[0].replace("#@title ", "") for k in cells]
    for want in ("B0", "B4", "B5", "C0b", "C1", "D1"):
        assert want in titles, want
    assert titles.index("B0") < titles.index("B5") < titles.index("C0b") < titles.index("C1") < titles.index("D1")


def test_notebook_cpu_cells_run_end_to_end_in_smoke_mode(tmp_path, monkeypatch):
    """Runs setup, repo, B0, B2, B3, B4, B5 and C0b with the network/Drive/GPU parts stubbed."""
    import subprocess

    monkeypatch.setenv("ROOTIQ_AI_HOME", str(tmp_path / "ai"))
    monkeypatch.setenv("ROOTIQ_REPO", str(TRAINING.parent))
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: None)   # no git clone / pull
    nb, cells = _cells()
    ns: dict = {"__name__": "notebook"}
    old_path = list(sys.path)
    try:
        for prefix in ("#@title 1)", "#@title 3)", "#@title B0)"):
            exec(compile(_cell(cells, prefix), prefix, "exec"), ns)
        ns["teacher"] = lambda *a, **k: None                       # stands in for B1 (needs a Groq key)
        for prefix in ("#@title B2)", "#@title B3)", "#@title B4)", "#@title B5)", "#@title C0b)"):
            exec(compile(_cell(cells, prefix), prefix, "exec"), ns)
    finally:
        sys.path[:] = old_path
    data = tmp_path / "ai" / "data"
    for name in ("train", "val", "eval_grounded", "kb_test_seen", "kb_test_unseen"):
        assert (data / f"{name}.jsonl").stat().st_size > 0, name
    train = [json.loads(l) for l in (data / "train.jsonl").read_text(encoding="utf-8").splitlines()]
    tasks = {r.get("task") for r in train}
    assert {"identify", "syslog", "command_lookup", "safety_refusal", "explain", "recommend"} <= tasks
    assert not any(t and str(t).startswith("ext_") for t in tasks)          # external data is off by default
    seen = {json.loads(l)["messages"][1]["content"] for l in (data / "kb_test_seen.jsonl").read_text(encoding="utf-8").splitlines()}
    assert not seen & {r["messages"][1]["content"] for r in train}, "KB test prompts leaked into the training file"
    assert len(ns["kb_seen_rows"]) > 0 and len(ns["kb_unseen_rows"]) > 0


def test_gpu_cells_at_least_compile_and_the_ship_rule_behaves(tmp_path):
    """C1/C2/D1/E1 need a GPU (not run here). They must compile, and D1's decision logic is exercised with stand-ins."""
    from types import SimpleNamespace

    nb, cells = _cells()
    for k, v in cells.items():
        compile(v, k, "exec")

    rows = load("test_seen")
    by_prompt = {r["messages"][1]["content"]: r["messages"][2]["content"] for r in rows}

    def make_ns(answer_fn):
        (tmp_path / "reports").mkdir(exist_ok=True)
        good_ccna = {"n": 40, "accuracy": 0.60, "single_answer_accuracy": 0.60}
        tuned = SimpleNamespace(eval=lambda: None, config=SimpleNamespace(use_cache=False))
        return {
            "trainer": SimpleNamespace(model=tuned), "generate": lambda *a, **k: "", "held_out_rows": [], "ccna": [],
            "mcq_accuracy": lambda fn, items: good_ccna,
            "grounding_eval": lambda fn, rows_: {"n": 12, "grounded_rate": 1.0, "keeps_headline_percent": 1.0, "correct_language": 1.0, "refusals": 0},
            "kb_evaluate": lambda m: {n: kb_eval.evaluate(rows, answer_fn) for n in ("seen", "unseen")},
            "kb_eval": kb_eval, "ROOT": tmp_path, "BASE": "stub", "MODEL_NAME": "stub", "SMOKE": False, "base_teacher": {},
            "save_json": lambda p, o: Path(p).write_text(json.dumps(o, default=str), encoding="utf-8"), "now": lambda: "now", "json": json,
            "before": {"ccna": good_ccna, "grounding": {"grounded_rate": 1.0},
                       "kb": {n: kb_eval.evaluate(rows, lambda m: "I am not sure.") for n in ("seen", "unseen")}},
        }

    good = make_ns(lambda msgs: by_prompt[msgs[1]["content"]])
    exec(compile(_cell(cells, "#@title D1)"), "D1", "exec"), good)
    assert good["report"]["decision"] == "SHIP" and all(good["kb_rules"].values())

    def unsafe(msgs):
        ans = by_prompt[msgs[1]["content"]]
        return ans + " Then run `reload` and `write erase`." if "read-only inspection" in ans else ans

    bad = make_ns(unsafe)
    exec(compile(_cell(cells, "#@title D1)"), "D1", "exec"), bad)
    assert bad["report"]["decision"] == "DO NOT SHIP" and bad["kb_rules"]["zero_unsafe_commands"] is False

    ignorant = make_ns(lambda msgs: "I am not sure.")
    exec(compile(_cell(cells, "#@title D1)"), "D1", "exec"), ignorant)
    assert ignorant["report"]["decision"] == "DO NOT SHIP" and ignorant["kb_rules"]["floors_met"] is False
