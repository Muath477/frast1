"""RootIQ collector — runs on COLLECTOR-01, polls every 2s and pushes event batches to the backend."""
import asyncio
import os
import re
import subprocess
import time
from datetime import datetime, timezone

import dns.resolver
import httpx

BACKEND = os.environ["ROOTIQ_BACKEND"]  # e.g. http://192.168.100.20:8000
TOKEN = os.environ["ROOTIQ_INGEST_TOKEN"]
COMMUNITY = os.environ.get("SNMP_COMMUNITY", "rootiq-ro")
INTERVAL = 2.0
# (device, mgmt_ip, interface, ifIndex, speed_mbps) — same values as topology.json
PORTS = [
    ("r1", "10.10.10.1", "Gi0/0", 1, 10),
    ("r1", "10.10.10.1", "Gi0/1", 2, 1000),
]
# per link: (near hop, far hop) for differential latency
HOPS = {
    "link-r1-sw2": (None, "10.10.30.1"),
    "link-r1-sw1": ("10.10.30.1", "10.10.20.11"),
    "link-sw1-app01": ("10.10.20.11", "10.10.20.10"),
}
OID = {
    "in": "1.3.6.1.2.1.31.1.1.1.6",
    "out": "1.3.6.1.2.1.31.1.1.1.10",
    "disc": "1.3.6.1.2.1.2.2.1.19",
    "oper": "1.3.6.1.2.1.2.2.1.8",
}
prev: dict = {}


def ev(source_id, source_type, metric, value, unit, interface=None, **meta):
    return {
        "sourceId": source_id,
        "sourceType": source_type,
        "metric": metric,
        "value": round(value, 3),
        "unit": unit,
        "interface": interface,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": meta,
    }


def snmpget(ip: str, oids: list[str]) -> list[int]:
    out = subprocess.run(
        ["snmpget", "-v2c", "-c", COMMUNITY, "-t", "1", "-r", "0", "-Oqv", ip, *oids],
        capture_output=True,
        text=True,
        timeout=3,
    )
    return [int(re.sub(r"\D", "", x) or 0) for x in out.stdout.split()]


def poll_ports():
    events, now = [], time.time()
    for dev, ip, ifname, idx, speed in PORTS:
        try:
            i, o, d, op = snmpget(
                ip,
                [
                    f'{OID["in"]}.{idx}',
                    f'{OID["out"]}.{idx}',
                    f'{OID["disc"]}.{idx}',
                    f'{OID["oper"]}.{idx}',
                ],
            )
        except Exception:
            events.append(ev(dev, "router", "poll_timeout", 1, "bool", ifname))
            continue
        key = (dev, ifname)
        if key in prev:
            t0, i0, o0, d0 = prev[key]
            dt = max(now - t0, 0.5)
            util = max(i - i0, o - o0) * 8 / (dt * speed * 1e6) * 100
            events += [
                ev(
                    dev,
                    "router",
                    "link_utilization",
                    min(util, 100),
                    "percent",
                    ifname,
                    collector="snmp",
                ),
                ev(
                    dev,
                    "router",
                    "if_out_discards_rate",
                    max(d - d0, 0) / dt,
                    "pps",
                    ifname,
                    collector="snmp",
                ),
            ]
        events.append(
            ev(dev, "router", "if_oper_status", 1 if op == 1 else 0, "bool", ifname, collector="snmp")
        )
        prev[key] = (now, i, o, d)
    return events


def ping(ip: str) -> tuple[float, float]:
    out = subprocess.run(
        ["ping", "-n", "-q", "-c", "5", "-i", "0.2", "-W", "1", ip],
        capture_output=True,
        text=True,
    ).stdout
    loss_m = re.search(r"([\d.]+)% packet loss", out)
    loss = float(loss_m.group(1)) if loss_m else 100.0
    m = re.search(r"= [\d.]+/([\d.]+)/", out)
    return (float(m.group(1)) if m else 1000.0), loss


def poll_hops():
    rtt = {}
    for ip in {"10.10.30.1", "10.10.20.11", "10.10.20.10"}:
        rtt[ip] = ping(ip)
    events = []
    for link, (near, far) in HOPS.items():
        lat_far, loss_far = rtt[far]
        lat_near, loss_near = rtt[near] if near else (0.0, 0.0)
        events += [
            ev(
                link,
                "link",
                "link_latency_ms",
                max(lat_far - lat_near, 0),
                "ms",
                collector="icmp",
            ),
            ev(
                link,
                "link",
                "link_packet_loss",
                max(loss_far - loss_near, 0),
                "percent",
                collector="icmp",
            ),
        ]
    return events


def poll_services():
    events = []
    r = dns.resolver.Resolver(configure=False)
    r.nameservers = ["10.10.20.10"]
    r.lifetime = 1.0
    ok, t0 = 0, time.perf_counter()
    for _ in range(5):
        try:
            r.resolve("app.rootiq.lab", "A")
            ok += 1
        except Exception:
            pass
    events += [
        ev("svc-dns", "service", "dns_success_rate", ok * 20, "percent", collector="dns"),
        ev(
            "svc-dns",
            "service",
            "dns_latency_ms",
            (time.perf_counter() - t0) * 1000 / 5,
            "ms",
            collector="dns",
        ),
    ]
    try:
        ip = r.resolve("app.rootiq.lab", "A")[0].to_text()
        t0 = time.perf_counter()
        resp = httpx.get(f"http://{ip}/health", headers={"Host": "app.rootiq.lab"}, timeout=2.0)
        events += [
            ev(
                "svc-web",
                "service",
                "http_ok",
                1 if resp.status_code == 200 else 0,
                "bool",
                collector="http",
            ),
            ev(
                "svc-web",
                "service",
                "http_latency_ms",
                (time.perf_counter() - t0) * 1000,
                "ms",
                collector="http",
            ),
        ]
    except Exception:
        events.append(ev("svc-web", "service", "http_ok", 0, "bool", collector="http"))
    try:
        h = httpx.get("http://10.10.20.10:9100/metrics", timeout=1.5).json()
        events += [
            ev("app01", "server", "cpu_percent", h["cpu"], "percent", collector="agent"),
            ev("app01", "server", "mem_percent", h["mem"], "percent", collector="agent"),
        ]
    except Exception:
        events.append(ev("app01", "server", "poll_timeout", 1, "bool", collector="agent"))
    return events


async def main():
    async with httpx.AsyncClient(timeout=3.0) as client:
        while True:
            t0 = time.time()
            batch = await asyncio.gather(
                *(asyncio.to_thread(f) for f in (poll_ports, poll_hops, poll_services))
            )
            events = [e for part in batch for e in part]
            try:
                await client.post(
                    f"{BACKEND}/api/events/batch",
                    json={"events": events},
                    headers={"x-rootiq-token": TOKEN},
                )
            except Exception as ex:
                print("push failed:", ex)
            await asyncio.sleep(max(0.0, INTERVAL - (time.time() - t0)))


if __name__ == "__main__":
    asyncio.run(main())
