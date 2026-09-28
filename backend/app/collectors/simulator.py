import asyncio
import random
from datetime import datetime, timezone

from app.schemas.event import Event

BASELINE = [
    ("link-r1-sw1", "link", "link_utilization", "percent", 14, 3),
    ("link-r1-sw1", "link", "link_latency_ms", "ms", 2.5, 0.6),
    ("link-r1-sw1", "link", "link_packet_loss", "percent", 0, 0),
    ("link-r1-sw1", "link", "if_out_discards_rate", "pps", 0, 0),
    ("link-r1-sw2", "link", "link_utilization", "percent", 6, 2),
    ("link-r1-sw2", "link", "link_latency_ms", "ms", 1.2, 0.3),
    ("link-sw1-app01", "link", "link_utilization", "percent", 9, 2),
    ("link-sw1-app01", "link", "link_latency_ms", "ms", 0.8, 0.2),
    ("link-sw2-collector01", "link", "link_utilization", "percent", 5, 1),
    ("app01", "server", "cpu_percent", "percent", 18, 4),
    ("app01", "server", "mem_percent", "percent", 41, 1),
    ("svc-web", "service", "http_latency_ms", "ms", 42, 8),
    ("svc-web", "service", "http_ok", "bool", 1, 0),
    ("svc-dns", "service", "dns_success_rate", "percent", 100, 0),
    ("svc-dns", "service", "dns_latency_ms", "ms", 4, 1),
]

SCENARIOS = {
    "uplink-congestion": [
        (0, "link-r1-sw1", "link_utilization", 97, 4),
        (1, "link-r1-sw1", "if_out_discards_rate", 180, 4),
        (2, "link-r1-sw1", "link_latency_ms", 86, 6),
        (3, "link-r1-sw1", "link_packet_loss", 2.4, 6),
        (6, "svc-web", "http_latency_ms", 1450, 6),
        (8, "svc-dns", "dns_success_rate", 72, 5),
        (8, "svc-dns", "dns_latency_ms", 620, 5),
    ],
    "dns-failure": [
        (0, "svc-dns", "dns_success_rate", 0, 2),
        (0, "svc-dns", "dns_latency_ms", 1000, 2),
        (2, "svc-web", "http_ok", 0, 1),
    ],
    "server-spike": [
        (0, "app01", "cpu_percent", 98, 5),
        (1, "app01", "mem_percent", 78, 8),
        (4, "svc-web", "http_latency_ms", 1100, 6),
        (6, "svc-dns", "dns_latency_ms", 160, 6),
    ],
}


class Simulator:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.current = {(e, m): b for e, _, m, _, b, _ in BASELINE}
        self.active: str | None = None
        self.elapsed = 0.0
        self.recovering = False
        self.paused = False

    def inject(self, scenario: str):
        assert scenario in SCENARIOS
        self.active, self.elapsed, self.recovering = scenario, 0.0, False

    def remediate(self):
        self.recovering = True

    def reset(self):
        self.active, self.recovering = None, False
        self.current = {(e, m): b for e, _, m, _, b, _ in BASELINE}

    def _target(self, e, m, base):
        if not self.active or self.recovering:
            return base, 8.0
        for off, te, tm, tgt, ramp in SCENARIOS[self.active]:
            if te == e and tm == m and self.elapsed >= off:
                return tgt, ramp
        return base, 4.0

    async def run(self, tick: float = 1.0):
        while True:
            await asyncio.sleep(tick)
            if self.paused:
                continue
            self.elapsed += tick
            now = datetime.now(timezone.utc)
            for e, st, m, unit, base, noise in BASELINE:
                tgt, ramp = self._target(e, m, base)
                cur = self.current[(e, m)]
                cur += (tgt - cur) * min(1.0, tick / ramp)
                self.current[(e, m)] = cur
                val = max(0.0, cur + random.gauss(0, noise))
                if unit == "percent":
                    val = min(val, 100.0)
                if unit == "bool":
                    val = 1.0 if cur >= 0.5 else 0.0
                await self.pipeline.ingest(
                    Event(
                        source_id=e,
                        source_type=st,
                        metric=m,
                        value=round(val, 2),
                        unit=unit,
                        timestamp=now,
                        metadata={"collector": "simulator"},
                    )
                )
