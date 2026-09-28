import asyncio
from collections import defaultdict, deque

from app.intelligence.thresholds import static_severity
from app.services.hub import hub

LINK_FIELDS = {
    "link_utilization": "utilization",
    "link_latency_ms": "latencyMs",
    "link_packet_loss": "packetLoss",
}


def sev_to_status(sev: float) -> str:
    return "critical" if sev >= 1 else "warning" if sev >= 0.5 else "healthy"


class StateStore:
    def __init__(self, topo):
        self.topo = topo
        self.metrics: dict[str, dict[str, float]] = defaultdict(dict)
        self.history: dict[str, deque] = defaultdict(lambda: deque(maxlen=300))
        self.dirty: set[str] = set()

    def kind(self, entity: str) -> str:
        if entity in self.topo.links:
            return "link"
        if entity in self.topo.services:
            return "service"
        return "node"

    def update(self, source_id: str, metric: str, value: float, ts: float):
        self.metrics[source_id][metric] = value
        self.history[f"{source_id}|{metric}"].append((ts, value))
        self.dirty.add(source_id)

    def status(self, entity: str) -> str:
        return sev_to_status(
            max((static_severity(m, v) for m, v in self.metrics[entity].items()), default=0)
        )

    def payload(self, entity: str) -> dict:
        m = self.metrics[entity]
        if self.kind(entity) == "link":
            return {
                "id": entity,
                "status": self.status(entity),
                **{camel: round(m.get(k, 0.0), 2) for k, camel in LINK_FIELDS.items()},
            }
        return {
            "id": entity,
            "status": self.status(entity),
            "metrics": {k: round(v, 2) for k, v in m.items()},
        }

    def link_metrics(self, link_id: str, minutes: float = 5) -> dict:
        import time

        cutoff = time.time() - minutes * 60
        out: dict[str, list] = {"utilization": [], "latencyMs": [], "packetLoss": []}
        mapping = {
            "link_utilization": "utilization",
            "link_latency_ms": "latencyMs",
            "link_packet_loss": "packetLoss",
        }
        for metric, key in mapping.items():
            for ts, v in self.history[f"{link_id}|{metric}"]:
                if ts >= cutoff:
                    out[key].append([ts, v])
        return out

    async def flush_loop(self):
        while True:
            await asyncio.sleep(1.0)
            dirty, self.dirty = self.dirty, set()
            for e in dirty:
                await hub.broadcast(self.kind(e), self.payload(e))
