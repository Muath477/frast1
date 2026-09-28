"""Day 13 emergency drills — each path must complete in < 30s."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000/api"
LIMIT = 30.0


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
    except Exception as e:
        return 0, {"error": str(e)}


def timed(name: str, fn):
    t0 = time.perf_counter()
    fn()
    dt = time.perf_counter() - t0
    status = "PASS" if dt < LIMIT else "FAIL"
    print(f"[{status}] {name}: {dt:.2f}s (limit {LIMIT:.0f}s)")
    if dt >= LIMIT:
        raise SystemExit(f"drill too slow: {name}")
    return dt


def drill_eve_failover_to_sim():
    """Presenter line → POST mode=sim → badge/mode is sim."""
    code, demo = call("POST", "/demo/mode", {"mode": "sim"})
    assert code == 200, demo
    assert demo.get("mode") == "sim"
    _, health = call("GET", "/health")
    assert health.get("mode") == "sim"


def drill_alternate_scenario():
    """Judge asks non-uplink → Shift+R then Shift+2 (reset + dns inject)."""
    code, _ = call("POST", "/demo/reset")
    assert code == 200
    code, demo = call("POST", "/demo/inject/dns-failure")
    assert code == 200, demo
    assert demo.get("scenario") == "dns-failure"
    assert demo.get("state") == "injected"


def drill_backend_health_recover():
    """Health must answer fast (ops: docker compose restart backend)."""
    code, health = call("GET", "/health")
    assert code == 200 and health.get("status") == "ok"


def drill_rca_wrong_talking_point():
    """Ensure a multi-candidate incident exists for the CandidateRanking line."""
    call("POST", "/demo/reset")
    time.sleep(0.8)
    call("POST", "/demo/inject/uplink-congestion")
    for _ in range(45):
        time.sleep(1)
        _, items = call("GET", "/incidents")
        open_ = [x for x in items if x.get("status") != "resolved" and x.get("candidates")]
        if open_ and len(open_[0].get("candidates") or []) >= 2:
            call("POST", "/demo/reset")
            return
    raise AssertionError("no multi-candidate incident for talking point")


def main():
    print("RootIQ emergency drills (Day 13)")
    timed("EVE hang -> switch to SIMULATION", drill_eve_failover_to_sim)
    timed("Backend health probe (restart path)", drill_backend_health_recover)
    timed("Judge asks other scenario (reset+DNS)", drill_alternate_scenario)
    # Talking-point content check (may take RCA window; not the <30s muscle-memory path)
    t0 = time.perf_counter()
    drill_rca_wrong_talking_point()
    print(f"[PASS] Wrong-RCA talking point (candidates ready): {time.perf_counter()-t0:.1f}s")
    print("WIFI: N/A — all local (localhost). Laptop failover: spare laptop / video — bag checklist.")
    print("DAY13_DRILLS_OK")


if __name__ == "__main__":
    main()
