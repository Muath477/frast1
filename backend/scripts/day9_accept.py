"""Day 9 sim: run each scenario once through inject → RCA → approve → recover."""
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
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def wait_pending(timeout=45):
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


def run_one(scenario: str, expected: str) -> dict:
    call("POST", "/demo/reset")
    time.sleep(1)
    call("POST", f"/demo/inject/{scenario}")
    inc = wait_pending()
    assert inc, f"{scenario}: no RCA/action"
    root = inc["rootCause"]["entityId"]
    assert root == expected, f"{scenario}: got {root} want {expected}"
    aid = inc["action"]["id"]
    iid = inc["id"]
    # reject then approve
    code, _ = call("POST", f"/actions/{aid}/reject", {"decidedBy": "Ahmed", "reason": "x"})
    assert code == 422
    code, repl = call(
        "POST",
        f"/actions/{aid}/reject",
        {"decidedBy": "Ahmed", "reason": "Outside change window"},
    )
    assert code == 200
    aid2 = repl["id"]
    code, ap = call("POST", f"/actions/{aid2}/approve", {"decidedBy": "Ahmed"})
    assert code == 200 and ap.get("approvalStatus") == "executed"
    for _ in range(40):
        time.sleep(1)
        _, cur = call("GET", f"/incidents/{iid}")
        if cur.get("status") == "resolved":
            noise = 1 - 1 / max(cur.get("rawAlertCount") or 1, 1)
            t = cur["timings"]
            inj = t.get("injectedAt")
            ana = t.get("analyzedAt")
            ttr = None
            if inj and ana:
                from datetime import datetime

                ttr = (
                    datetime.fromisoformat(ana.replace("Z", "+00:00"))
                    - datetime.fromisoformat(inj.replace("Z", "+00:00"))
                ).total_seconds()
            return {
                "scenario": scenario,
                "root": root,
                "correct": True,
                "noise": noise,
                "ttr": ttr,
                "raw": cur.get("rawAlertCount"),
            }
    raise AssertionError(f"{scenario}: not resolved")


def main():
    results = []
    for sc, exp in SCENARIOS.items():
        r = run_one(sc, exp)
        results.append(r)
        print(
            f"OK {sc} root={r['root']} noise={r['noise']:.1%} ttr={r['ttr']:.1f}s raw={r['raw']}"
        )
    _, runs = call("GET", "/runs")
    s = runs["summary"]
    print("summary", s)
    assert s["top1Accuracy"] == 1.0
    assert s["avgTimeToRootCause"] is not None and s["avgTimeToRootCause"] < 60
    if results[0]["noise"] < 0.8:
        raise AssertionError("uplink noise reduction < 80%")
    print("DAY9_OK")


if __name__ == "__main__":
    main()
