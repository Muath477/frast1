from fastapi import HTTPException

from app.schemas.event import Event


class Pipeline:
    def __init__(self, topo, state):
        self.topo = topo
        self.state = state
        self.known = set(topo.nodes) | set(topo.links) | set(topo.services)

    async def ingest(self, ev: Event):
        if (
            ev.source_type in ("router", "switch")
            and ev.interface
            and ev.metric.startswith(("link_", "if_"))
        ):
            link = self.topo.port_to_link.get((ev.source_id, ev.interface))
            if link:
                ev.source_id, ev.source_type = link, "link"
        if ev.source_id not in self.known:
            raise HTTPException(status_code=422, detail=f"unknown sourceId {ev.source_id}")
        self.state.update(ev.source_id, ev.metric, ev.value, ev.timestamp.timestamp())
