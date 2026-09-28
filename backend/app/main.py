import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import events, health, topology, ws
from app.collectors.simulator import Simulator
from app.core.config import settings
from app.services.pipeline import Pipeline
from app.services.state_store import StateStore
from app.services.topology_service import TopologyService


def build_snapshot(app: FastAPI) -> dict:
    topo: TopologyService = app.state.topology
    state: StateStore = app.state.state
    snap = topo.snapshot()

    for n in snap["nodes"]:
        if n["id"] in state.metrics:
            p = state.payload(n["id"])
            n["status"] = p["status"]
            n["metrics"] = p.get("metrics", {})

    for l in snap["links"]:
        if l["id"] in state.metrics:
            p = state.payload(l["id"])
            l["status"] = p["status"]
            l["utilization"] = p.get("utilization", 0)
            l["latencyMs"] = p.get("latencyMs", 0)
            l["packetLoss"] = p.get("packetLoss", 0)

    for s in snap["services"]:
        if s["id"] in state.metrics:
            p = state.payload(s["id"])
            s["status"] = p["status"]
            s["metrics"] = p.get("metrics", {})

    demo = {
        "mode": settings.rootiq_mode if settings.rootiq_mode in ("live", "sim") else "sim",
        "scenario": None,
        "state": "idle",
    }
    sim: Simulator | None = getattr(app.state, "simulator", None)
    if sim is not None:
        demo["scenario"] = sim.active
        if sim.recovering:
            demo["state"] = "remediating"
        elif sim.active:
            demo["state"] = "injected"

    return {
        "topology": snap,
        "incidents": [],
        "alerts": [],
        "demo": demo,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    topo = TopologyService()
    state = StateStore(topo)
    pipeline = Pipeline(topo, state)
    app.state.topology = topo
    app.state.state = state
    app.state.pipeline = pipeline
    app.state.snapshot = lambda: build_snapshot(app)
    app.state.tasks = [asyncio.create_task(state.flush_loop())]

    if settings.rootiq_mode == "sim":
        sim = Simulator(pipeline)
        sim.paused = settings.sim_paused
        app.state.simulator = sim
        app.state.tasks.append(asyncio.create_task(sim.run()))

    yield

    for t in app.state.tasks:
        t.cancel()


app = FastAPI(title="RootIQ API", version="0.1.0", lifespan=lifespan)
app.include_router(health.router, prefix="/api")
app.include_router(topology.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(ws.router)
