import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api import actions, demo, events, health, incidents, topology, ws
from app.collectors.simulator import Simulator
from app.core.config import settings
from app.intelligence.correlate import Correlator
from app.intelligence.detector import Detector
from app.intelligence.graph import TopologyGraph
from app.intelligence.history import History
from app.services.action_service import ActionService
from app.services.audit import AuditLog
from app.services.incident_service import IncidentService, IncidentState
from app.services.pipeline import Pipeline
from app.services.recorder import Recorder
from app.services.state_store import StateStore
from app.services.topology_service import TopologyService
from app.db import Base, engine
from app.db.persist import upsert_incident


def _persist_path() -> Path:
    p = Path(__file__).resolve().parents[2] / "data" / "incidents.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _history_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "history.json"


def make_persist(_holder: dict):
    def persist(inc):
        path = _persist_path()
        existing = []
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
        blob = inc.to_dict()
        existing = [i for i in existing if i["id"] != blob["id"]]
        existing.insert(0, blob)
        path.write_text(json.dumps(existing[:100], indent=2), encoding="utf-8")
        try:
            upsert_incident(inc)
        except Exception:
            pass

    return persist


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

    return {
        "topology": snap,
        "incidents": app.state.incidents.list_incidents(),
        "alerts": list(app.state.pipeline.alerts),
        "demo": app.state.demo,
    }


async def recovery_loop(app: FastAPI):
    while True:
        await asyncio.sleep(1.0)
        try:
            await app.state.actions.recovery_tick()
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    topo = TopologyService()
    state = StateStore(topo)
    detector = Detector()
    graph = TopologyGraph(topo.raw)
    correlator = Correlator(graph)
    history = History(str(_history_path()))
    audit = AuditLog()

    demo_state = {
        "mode": "sim" if settings.rootiq_mode == "sim" else "live",
        "scenario": None,
        "state": "idle",
        "injectedAt": None,
    }

    holder: dict = {}
    incidents_svc = IncidentService(
        correlator,
        graph,
        demo_ref=lambda: demo_state,
        history=history,
        persist=make_persist(holder),
        topology=topo,
    )

    path = _persist_path()
    if path.exists():
        for blob in json.loads(path.read_text(encoding="utf-8")):
            st = IncidentState(
                blob["id"],
                blob["title"],
                blob["openedAt"],
                (blob.get("timings") or {}).get("injectedAt"),
            )
            st.status = blob.get("status", "resolved")
            st.severity = blob.get("severity", "high")
            st.resolved_at = blob.get("resolvedAt")
            st.members = set(blob.get("members") or [])
            st.evidence = blob.get("evidence") or []
            st.raw_alert_count = blob.get("rawAlertCount") or 0
            st.affected_services = blob.get("affectedServices") or []
            st.timings = blob.get("timings") or st.timings
            st.root_cause = blob.get("rootCause")
            st.candidates = blob.get("candidates") or []
            st.cause_path = blob.get("causePath") or []
            st.impact_path = blob.get("impactPath") or []
            st.explanation = blob.get("explanation")
            st.action = blob.get("action")
            st.needs_investigation = blob.get("needsInvestigation", True)
            if st.status != "resolved":
                incidents_svc.open[st.id] = st
            else:
                incidents_svc.history_list.append(st)

    action_svc = ActionService(
        incidents_svc,
        demo_ref=lambda: demo_state,
        detector=detector,
        history=history,
        simulator_ref=lambda: getattr(app.state, "simulator", None),
        audit=audit,
    )
    incidents_svc.actions = action_svc

    pipeline = Pipeline(topo, state, detector, incidents_svc)
    pipeline.recorder = Recorder()

    app.state.topology = topo
    app.state.state = state
    app.state.detector = detector
    app.state.incidents = incidents_svc
    app.state.actions = action_svc
    app.state.audit = audit
    app.state.history = history
    app.state.pipeline = pipeline
    app.state.demo = demo_state
    app.state.snapshot = lambda: build_snapshot(app)
    app.state.tasks = [
        asyncio.create_task(state.flush_loop()),
        asyncio.create_task(recovery_loop(app)),
    ]

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
app.include_router(demo.router, prefix="/api")
app.include_router(incidents.router, prefix="/api")
app.include_router(actions.router, prefix="/api")
app.include_router(ws.router)
