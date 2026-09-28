"""UDP syslog listener (port 514) — optional side task for the live collector."""
from __future__ import annotations

import asyncio
import re
from datetime import datetime, timezone

# Rough Cisco interface → lab link map (extend after CDP discovery)
IF_TO_LINK = {
    "GigabitEthernet0/0": "link-r1-sw1",
    "Gi0/0": "link-r1-sw1",
    "GigabitEthernet0/1": "link-r1-sw2",
    "Gi0/1": "link-r1-sw2",
}

LINK_RE = re.compile(
    r"%(?:LINK-3-UPDOWN|LINEPROTO-5-UPDOWN).*?(?:Interface|interface)\s+(\S+).*?(?:down|up)",
    re.I,
)


def parse_syslog(msg: str) -> dict | None:
    m = LINK_RE.search(msg)
    if not m:
        if "%QOS" in msg.upper():
            return {
                "sourceId": "link-r1-sw1",
                "sourceType": "link",
                "metric": "syslog_qos",
                "value": 1.0,
                "unit": "bool",
            }
        return None
    iface = m.group(1).rstrip(",")
    link = IF_TO_LINK.get(iface)
    if not link:
        return None
    down = "down" in m.group(0).lower().split()[-1] or "changed state to down" in msg.lower()
    return {
        "sourceId": link,
        "sourceType": "link",
        "metric": "syslog_link_down",
        "value": 1.0 if down else 0.0,
        "unit": "bool",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": {"collector": "syslog", "raw": msg[:200]},
    }


class SyslogProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def datagram_received(self, data: bytes, addr):
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            return
        ev = parse_syslog(text)
        if ev:
            self.queue.put_nowait(ev)


async def start_syslog(queue: asyncio.Queue, host: str = "0.0.0.0", port: int = 514):
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: SyslogProtocol(queue),
        local_addr=(host, port),
    )
    return transport
