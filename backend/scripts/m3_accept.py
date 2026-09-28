"""One-shot Day 8 / M3 acceptance against a running backend."""
import json
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000/api"


def call(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if body is not None:
        req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode() or "null"
            return r.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode() or "{}"
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}


def main():
    call("POST", "/demo/reset")
    time.sleep(1)
    call("POST", "/demo/inject/uplink-congestion")

    inc = None
    for _ in range(45):
        time.sleep(1)
        _, items = call("GET", "/incidents")
        open_ = [
            x
            for x in items
            if x.get("status") != "resolved"
            and (x.get("action") or {}).get("approvalStatus") == "pending"
        ]
        if open_:
            inc = open_[0]
            break
    assert inc, "no pending action"
    aid = inc["action"]["id"]
    iid = inc["id"]
    print(
        f"incident={iid} action={aid} root={inc['rootCause']['entityId']} status={inc['status']}"
    )

    code, _ = call("POST", f"/actions/{aid}/reject", {"decidedBy": "Ahmed", "reason": "x"})
    print("reject_short", code)
    assert code == 422

    code, rej = call(
        "POST",
        f"/actions/{aid}/reject",
        {"decidedBy": "Ahmed", "reason": "Outside change window"},
    )
    # API returns the replacement pending action (rejected original stays in audit)
    print("reject", code, rej.get("approvalStatus"), rej.get("id"))
    assert code == 200 and rej.get("approvalStatus") == "pending"
    _, audit = call("GET", "/audit")
    print("audit", len(audit), audit[0]["action"] if audit else None)
    assert any(a["action"] == "reject" for a in audit)

    _, inc2 = call("GET", f"/incidents/{iid}")
    aid2 = inc2["action"]["id"]
    print("new_pending", aid2, inc2["action"]["approvalStatus"])
    assert aid2 == rej["id"] and inc2["action"]["approvalStatus"] == "pending"

    code, ap = call("POST", f"/actions/{aid2}/approve", {"decidedBy": "Ahmed"})
    print("approve", code, ap.get("approvalStatus"), ap.get("executedAt"))
    assert code == 200 and ap.get("approvalStatus") in ("executed", "approved", "failed")

    resolved = None
    for i in range(50):
        time.sleep(1)
        _, cur = call("GET", f"/incidents/{iid}")
        if cur.get("status") == "resolved":
            resolved = cur
            break
        if i % 5 == 0:
            act = (cur.get("action") or {}).get("approvalStatus")
            print(f"t={i} status={cur.get('status')} act={act}")
    assert resolved, "not resolved"
    t = resolved["timings"]
    print(
        "timings",
        {
            k: t.get(k)
            for k in (
                "injectedAt",
                "detectedAt",
                "analyzedAt",
                "decidedAt",
                "executedAt",
                "recoveredAt",
            )
        },
    )
    assert t.get("analyzedAt") and t.get("executedAt") and t.get("recoveredAt")

    _, runs = call("GET", "/runs")
    print("runs", runs["summary"]["count"], runs["runs"][-1]["metrics"] if runs["runs"] else None)
    print("M3_OK")


if __name__ == "__main__":
    main()
