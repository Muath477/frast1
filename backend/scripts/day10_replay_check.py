import json
import time
import urllib.request

BASE = "http://127.0.0.1:8000/api"


def call(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if body is not None:
        req.add_header("content-type", "application/json")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode() or "null")


call("POST", "/demo/reset")
time.sleep(0.5)
call("POST", "/demo/inject/uplink-congestion")
inc = None
for _ in range(30):
    time.sleep(1)
    items = call("GET", "/incidents")
    open_ = [x for x in items if x.get("status") != "resolved"]
    if open_:
        inc = open_[0]
        if inc.get("rootCause"):
            break
assert inc, "no incident"
rep = call("GET", f"/incidents/{inc['id']}/replay")
print("id", inc["id"], "steps", len(rep["steps"]), [s["kind"] for s in rep["steps"][:8]])
assert len(rep["steps"]) >= 2
print("REPLAY_OK")
