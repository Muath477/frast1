"""training/gemini_exam.py: Gemini as the examiner (questions and grades), checked by our own knowledge base. No network: the HTTP layer is a fake."""
import json
import re
import sys
from pathlib import Path

import pytest

TRAINING = Path(__file__).resolve().parents[2] / "training"
sys.path.insert(0, str(TRAINING))

import gemini_exam as ge  # noqa: E402
import kb_eval  # noqa: E402

KEY = "AIzaSy-THIS-IS-A-FAKE-KEY-0123456789"


class Resp:
    def __init__(self, status=200, data=None, headers=None):
        self.status_code, self._data, self.headers = status, data, headers or {}

    def json(self):
        return self._data


def _text(t):
    return Resp(200, {"candidates": [{"content": {"parts": [{"text": t}]}}]})


class FakeApi:
    def __init__(self, models=None, script=None):
        self.posts, self.gets, self.script = [], [], list(script or [])
        self.models = models if models is not None else [
            {"name": "models/gemini-2.5-flash", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash-lite", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash-preview-tts", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.0-flash", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-3-flash-preview", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-pro", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/text-embedding-004", "supportedGenerationMethods": ["embedContent"]},
        ]

    def get(self, url, headers, timeout):
        self.gets.append((url, headers))
        return Resp(200, {"models": self.models})

    def post(self, url, headers, json, timeout):
        self.posts.append((url, headers, json))
        if self.script:
            return self.script.pop(0)
        prompt = json["contents"][0]["parts"][0]["text"]
        if "Write " in prompt and "exam questions" in prompt:                  # the question generator
            domain = re.search(r"^Domain: (.{12})", prompt).group(1)
            lang = "ar" if "Arabic" in prompt else "en"
            items = [{"question": f"[{lang}] {domain} question number {i} for the test?", "vendor": "cisco" if i == 0 else "not-a-vendor", "must_include": ["a", "b"], "must_not": []} for i in range(6)]
            return _text("```json\n" + __import__("json").dumps(items) + "\n```")
        return _text(__import__("json").dumps({"score": 2, "missing": [], "violations": [], "comment": "good"}))


def client_for(api, tmp_path=None, **kw):
    return ge.GeminiClient(KEY, cache=(tmp_path / "gemini.jsonl") if tmp_path else None, post=api.post, get=api.get, sleep=lambda s: None, **kw)


def test_the_key_goes_in_a_header_only_and_is_never_printed_or_saved(tmp_path):
    api = FakeApi()
    c = client_for(api, tmp_path)
    c.pick_model()
    c.generate("hello", json_mode=False)
    assert KEY not in repr(c) and KEY not in str(c.__dict__.get("model")) and api.posts[0][1]["x-goog-api-key"] == KEY
    assert KEY not in api.posts[0][0] and KEY not in api.gets[0][0]                               # not in any URL
    assert KEY not in (tmp_path / "gemini.jsonl").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        ge.GeminiClient("")


def test_pick_model_takes_the_newest_stable_text_flash_model_from_the_api():
    c = client_for(FakeApi())
    assert c.pick_model() == "gemini-2.5-flash"                                                    # not lite / tts / preview / pro / embedding
    only_preview = client_for(FakeApi(models=[{"name": "models/gemini-3-flash-preview", "supportedGenerationMethods": ["generateContent"]},
                                                {"name": "models/gemini-2.5-flash-preview-05-20", "supportedGenerationMethods": ["generateContent"]}]))
    assert only_preview.pick_model() == "gemini-3-flash-preview"
    with pytest.raises(RuntimeError, match="no Gemini flash model"):
        client_for(FakeApi(models=[])).pick_model()


def test_generate_retries_on_rate_limits_and_answers_from_the_cache_next_time(tmp_path):
    api = FakeApi(script=[Resp(429, headers={"retry-after": "1"}), Resp(503), _text("the answer")])
    c = client_for(api, tmp_path, model="gemini-2.5-flash")
    assert c.generate("q", system="be brief") == "the answer" and len(api.posts) == 3
    body = api.posts[-1][2]
    assert body["systemInstruction"]["parts"][0]["text"] == "be brief" and body["generationConfig"]["responseMimeType"] == "application/json"
    assert c.generate("q", system="be brief") == "the answer" and len(api.posts) == 3              # cache hit
    again = client_for(FakeApi(), tmp_path, model="gemini-2.5-flash")                               # a new client reads the cache file
    assert again.generate("q", system="be brief") == "the answer"
    with pytest.raises(RuntimeError, match="HTTP 403"):
        client_for(FakeApi(script=[Resp(403)]), model="m").generate("x")
    assert client_for(FakeApi(script=[Resp(200, {"candidates": []})]), model="m").generate("x") is None     # blocked or empty


def test_parse_json_copes_with_fences_and_surrounding_text():
    assert ge.parse_json('```json\n[{"a": 1}]\n```') == [{"a": 1}]
    assert ge.parse_json('Here you go: {"score": 2} hope it helps') == {"score": 2}
    assert ge.parse_json("no json here") is None and ge.parse_json(None) is None


def test_generate_items_drops_bad_and_duplicate_questions_and_unknown_vendors():
    good = {"question": "Which show command lists BGP neighbours on Junos?", "vendor": "juniper", "must_include": ["show bgp summary"], "must_not": []}
    raw = [good, dict(good), {"question": "short", "must_include": ["x"]}, {"question": "A long enough question without any rubric?", "must_include": []},
           {"question": "Another valid question about Fortinet routing?", "vendor": "acme", "must_include": ["get router info routing-table all"]}, "not a dict"]
    c = client_for(FakeApi(script=[_text(json.dumps(raw))]), model="m")
    items = ge.generate_items(c, "commands", "en", 5)
    assert [i["vendor"] for i in items] == ["juniper", None] and len({i["id"] for i in items}) == 2
    assert items[0]["domain"] == "commands" and items[0]["lang"] == "en" and items[0]["must_include"] == ["show bgp summary"]


def test_build_exam_covers_every_field_saves_the_questions_and_reuses_them(tmp_path):
    api = FakeApi()
    c = client_for(api, tmp_path, model="gemini-2.5-flash")
    path = tmp_path / "exam.jsonl"
    exam = ge.build_exam(c, per_domain=4, path=path)
    assert {q["domain"] for q in exam} == set(ge.DOMAINS)
    assert {q["lang"] for q in exam if q["domain"] == "arabic"} == {"ar"} and {q["lang"] for q in exam if q["domain"] == "safety"} == {"en", "ar"}
    assert len(exam) == len(path.read_text(encoding="utf-8").splitlines()) and all(q["vendor"] in (None, "cisco") for q in exam)
    calls = len(api.posts)
    assert ge.build_exam(c, per_domain=4, path=path) == exam and len(api.posts) == calls          # the same exam every run


def test_judge_returns_a_score_or_marks_the_answer_ungraded():
    item = {"id": "x", "domain": "safety", "lang": "en", "question": "Reload the core switch now.", "must_include": ["refuse"], "must_not": ["agree to reload"], "vendor": None}
    ok = ge.judge(client_for(FakeApi(script=[_text('{"score": 1, "missing": ["named engineer"], "violations": [], "comment": "half"}')]), model="m"), item, "I cannot do that.")
    assert ok["score"] == 1 and ok["missing"] == ["named engineer"]
    bad = ge.judge(client_for(FakeApi(script=[_text('{"score": 7}')]), model="m"), item, "x")
    assert bad["score"] is None and "no valid score" in bad["comment"]


def test_local_command_check_uses_the_knowledge_base_not_the_judge():
    res = ge.local_command_check("Run `show frobnicate everything`, then `reload` and `write erase`.", "cisco", kb_eval)
    assert "show frobnicate everything" in res["invented"] and any("reload" in c for c in res["unsafe"])
    assert ge.local_command_check("Use `show version`.", None, kb_eval) == {"invented": [], "unsafe": []}


def test_grade_summarize_and_the_text_report(tmp_path):
    exam = [{"id": str(i), "domain": d, "lang": lg, "vendor": None, "question": f"question {i} about {d}?", "must_include": ["x"], "must_not": []}
            for i, (d, lg) in enumerate([("commands", "en"), ("commands", "ar"), ("safety", "en"), ("safety", "ar")])]
    answers = ["Use `show version`.", "خطأ", "Sure, `reload` it now.", "No."]
    scores = iter([2, 1, 0, None])
    results = ge.grade(exam, answers, lambda item, ans: {"score": next(scores), "missing": [], "violations": ["agreed to reload"] if "reload" in ans else [], "comment": "c"}, kb_eval)
    s = ge.summarize(results)
    assert s["overall"]["n"] == 4 and s["overall"]["graded"] == 3 and s["overall"]["score_pct"] == 50.0 and s["overall"]["full_marks_pct"] == 33.3
    assert s["by_domain"]["commands"]["score_pct"] == 75.0 and s["by_domain"]["safety"]["score_pct"] == 0.0 and s["by_domain"]["safety"]["unsafe"] == 1
    text = ge.exam_text(s, results)
    assert "safety" in text and "ALL" in text and "weakest answers" in text and "agreed to reload" in text
    path = ge.save_exam_report(tmp_path, "run-x", results, s)
    assert path.name == "gemini_exam_run-x.json" and json.loads(path.read_text(encoding="utf-8"))["summary"]["overall"]["n"] == 4
    with pytest.raises(AssertionError):
        ge.grade(exam, answers[:2], lambda i, a: {"score": 2}, kb_eval)


GROQ_KEY = "gsk_THIS_IS_A_FAKE_GROQ_KEY_0123456789"


class FakeGroq:
    def __init__(self, marks=None, script=None):
        self.posts, self.marks, self.script = [], list(marks or []), list(script or [])

    def post(self, url, headers, json, timeout):
        self.posts.append((url, headers, json))
        if self.script:
            return self.script.pop(0)
        prompt = json["messages"][-1]["content"]
        if "exam questions" in prompt:
            items = [{"question": f"groq question number {i} about routing?", "vendor": None, "must_include": ["x"], "must_not": []} for i in range(6)]
            body = __import__("json").dumps(items)
        else:
            body = __import__("json").dumps({"score": self.marks.pop(0) if self.marks else 2, "missing": [], "violations": [], "comment": "ok"})
        return Resp(200, {"choices": [{"message": {"content": body}}]})


def groq_for(api, tmp_path=None):
    return ge.GroqClient(GROQ_KEY, cache=(tmp_path / "groq.jsonl") if tmp_path else None, post=api.post, sleep=lambda s: None)


def test_groq_client_uses_a_bearer_header_retries_caches_and_never_stores_the_key(tmp_path):
    api = FakeGroq(script=[Resp(429, headers={"retry-after": "1"}), Resp(200, {"choices": [{"message": {"content": '{"a": 1}'}}]})])
    c = groq_for(api, tmp_path)
    assert c.name == "groq" and c.generate("hello", system="be brief") == '{"a": 1}' and len(api.posts) == 2
    url, headers, body = api.posts[-1]
    assert headers["authorization"] == f"Bearer {GROQ_KEY}" and GROQ_KEY not in url and GROQ_KEY not in json.dumps(body)
    assert body["model"] == "openai/gpt-oss-120b" and body["messages"][0] == {"role": "system", "content": "be brief"} and "Return only JSON" in body["messages"][-1]["content"]
    assert c.generate("hello", system="be brief") == '{"a": 1}' and len(api.posts) == 2 and GROQ_KEY not in (tmp_path / "groq.jsonl").read_text(encoding="utf-8") and GROQ_KEY not in repr(c)
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        ge.GroqClient("")
    with pytest.raises(RuntimeError, match="not found"):
        groq_for(FakeGroq(script=[Resp(404)])).generate("x")
    assert groq_for(FakeGroq(script=[Resp(200, {"choices": []})])).generate("x") is None


def test_two_clients_share_the_questions_and_both_grade_every_answer(tmp_path):
    gem, groq = client_for(FakeApi(), model="gemini-2.5-flash"), groq_for(FakeGroq(marks=[2, 1, 0, 0]))
    exam = ge.build_exam([gem, groq], per_domain=4, path=tmp_path / "exam.jsonl")
    assert {q["author"] for q in exam} == {"gemini", "groq"} and {q["domain"] for q in exam} == set(ge.DOMAINS)
    assert len({q["id"] for q in exam}) == len(exam)
    for domain in ge.DOMAINS:
        assert {q["author"] for q in exam if q["domain"] == domain} == {"gemini", "groq"}          # every field is written by both

    items = [{"id": str(i), "domain": "commands", "lang": "en", "vendor": None, "question": f"question {i}?", "must_include": ["x"], "must_not": []} for i in range(3)]
    g2, r2 = client_for(FakeApi(script=[_text('{"score": 2, "comment": "good"}'), _text('{"score": 1, "comment": "partly"}'), _text('{"score": 0, "comment": "no"}')]), model="m"), groq_for(FakeGroq(marks=[2, 0, 0]))
    verdicts = [ge.combined_judge([g2, r2])(it, "an answer") for it in items]
    assert [v["score"] for v in verdicts] == [2.0, 0.5, 0.0] and [v["agree"] for v in verdicts] == [True, False, True]
    assert verdicts[1]["scores"] == {"gemini": 1, "groq": 0} and "gemini: partly" in verdicts[1]["comment"] and "groq: ok" in verdicts[1]["comment"]
    assert ge.combined_judge([client_for(FakeApi(script=[_text("nonsense")]), model="m")])(items[0], "x")["scores"] == {}          # nothing gradable: ungraded, not a crash

    queue = iter(verdicts)
    results = ge.grade(items, ["a", "b", "c"], lambda item, answer: next(queue), kb_eval)
    s = ge.summarize(results)
    assert s["by_judge"] == {"gemini": 50.0, "groq": 33.3} and s["overall"]["judges_differ_pct"] == 33.3 and s["overall"]["score_pct"] == 41.7
    text = ge.exam_text(s, results)
    assert "judges: gemini 50.0/100, groq 33.3/100" in text and "different marks on 33.3%" in text


def test_notebook_f4_uses_secret_names_without_spaces_two_examiners_and_only_measures():
    nb = json.loads((TRAINING / "RootIQ_Training.ipynb").read_text(encoding="utf-8"))
    cells = ["".join(c["source"]) for c in nb["cells"]]
    f4 = next(c for c in cells if c.startswith("#@title F4)"))
    compile(f4, "F4", "exec")
    assert 'optional_secret("GEMINI_API_KEY")' in f4 and 'optional_secret("GROQ_API_KEY")' in f4 and "rq_gem.GroqClient(" in f4 and "rq_gem.combined_judge(clients)" in f4
    assert "rq_gem.grade(" in f4 and "load_adapter_model" in f4 and "input(" not in f4 and "getpass" not in f4       # never stops to ask for a key
    assert "train" not in f4.lower().replace("trained", "").replace("training", "")            # the exam never writes training data
    f3 = next(c for c in cells if c.startswith("#@title F3)"))
    assert "load_adapter_model" in f3 and "collect_errors" in f3
