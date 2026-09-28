"""Day 12: 3 scenarios × 3 runs → print /api/runs summary for RESULTS.md."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000/api"
SCENARIOS = {
    "uplink-congestion": "link-r1-sw1",
    "dns-failure": "svc-dns",
    "server-spike": "app01",
}


def call(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if body is not None:
        req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def wait_pending(timeout=50):
    for _ in range(timeout):
        time.sleep(1)
        _, items = call("GET", "/incidents")
        open_ = [
            x
            for x in items
            if x.get("status") != "resolved"
            and (x.get("action") or {}).get("approvalStatus") == "pending"
            and x.get("rootCause")
        ]
        if open_:
            return open_[0]
    return None


def run_one(scenario: str, expected: str) -> None:
    call("POST", "/demo/reset")
    time.sleep(1.5)
    call("POST", f"/demo/inject/{scenario}")
    inc = wait_pending()
    assert inc, f"{scenario}: no RCA/action"
    root = (inc.get("rootCause") or {}).get("entityId")
    assert root == expected, f"{scenario}: got {root} want {expected}"
    aid = inc["action"]["id"]
    iid = inc["id"]
    code, repl = call(
        "POST",
        f"/actions/{aid}/reject",
        {"decidedBy": "Ahmed", "reason": "Outside change window"},
    )
    assert code == 200, repl
    aid2 = repl["id"]
    code, ap = call("POST", f"/actions/{aid2}/approve", {"decidedBy": "Ahmed"})
    assert code == 200 and ap.get("approvalStatus") == "executed", ap
    for _ in range(45):
        time.sleep(1)
        _, cur = call("GET", f"/incidents/{iid}")
        if cur.get("status") == "resolved":
            print(f"OK {scenario} root={root} raw={cur.get('rawAlertCount')}")
            return
    raise AssertionError(f"{scenario}: not resolved")


def main():
    call("POST", "/demo/reset")
    time.sleep(1)
    # Clear in-memory runs by restarting is ideal; here we just append 9 fresh
    for sc, exp in SCENARIOS.items():
        for i in range(3):
            print(f"--- {sc} run {i+1}/3 ---")
            run_one(sc, exp)
    _, runs = call("GET", "/runs")
    print(json.dumps(runs, indent=2))
    s = runs["summary"]
    assert s["count"] >= 9
    assert s["top1Accuracy"] == 1.0
    assert s["avgTimeToRootCause"] is not None and s["avgTimeToRootCause"] < 60
    print("DAY12_MEASURE_OK")


if __name__ == "__main__":
    main()
