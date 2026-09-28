import json
import os
import tempfile
from pathlib import Path

from app.core.config import settings


class TopologyError(RuntimeError):
    pass


class TopologyService:
    def __init__(self):
        self.raw = json.loads(Path(settings.topology_path).read_text(encoding="utf-8"))
        self._validate()
        self.nodes = {n["id"]: n for n in self.raw["nodes"]}
        self.links = {l["id"]: l for l in self.raw["links"]}
        self.services = {s["id"]: s for s in self.raw["services"]}
        self.port_to_link: dict[tuple[str, str], str] = {}
        for l in self.links.values():
            self.port_to_link[(l["source"], l["sourcePort"])] = l["id"]
            self.port_to_link[(l["target"], l["targetPort"])] = l["id"]
        self._apply_layout()

    def _validate(self):
        ids = {n["id"]: {i["name"] for i in n["interfaces"]} for n in self.raw["nodes"]}
        for l in self.raw["links"]:
            for end, port in ((l["source"], l["sourcePort"]), (l["target"], l["targetPort"])):
                if end not in ids or port not in ids[end]:
                    raise TopologyError(f"link {l['id']}: unknown endpoint {end}:{port}")
        for s in self.raw["services"]:
            if s["host"] not in ids:
                raise TopologyError(f"service {s['id']}: unknown host {s['host']}")

    def _apply_layout(self):
        p = Path(settings.layout_path)
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            # Support both flat {nid: {x,y}} and {positions: {...}}
            positions = data.get("positions", data) if isinstance(data, dict) else {}
            for nid, pos in positions.items():
                if nid in self.nodes and isinstance(pos, dict) and "x" in pos:
                    self.nodes[nid]["position"] = pos

    def save_layout(self, positions: dict[str, dict]):
        unknown = set(positions) - set(self.nodes)
        if unknown:
            raise TopologyError(f"unknown nodes: {sorted(unknown)}")
        for nid, pos in positions.items():
            self.nodes[nid]["position"] = {"x": float(pos["x"]), "y": float(pos["y"])}
        layout_path = Path(settings.layout_path)
        layout_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=layout_path.parent, suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({k: v["position"] for k, v in self.nodes.items()}, f, indent=2)
        os.replace(tmp, layout_path)

    def speed_of(self, link_id: str) -> int:
        l = self.links[link_id]
        src = next(
            i for i in self.nodes[l["source"]]["interfaces"] if i["name"] == l["sourcePort"]
        )
        return int(src["speedMbps"])

    def snapshot(self) -> dict:
        nodes = []
        for n in self.nodes.values():
            nodes.append({**n, "status": n.get("status", "healthy"), "metrics": n.get("metrics", {})})
        links = []
        for l in self.links.values():
            links.append(
                {
                    **l,
                    "speedMbps": self.speed_of(l["id"]),
                    "status": l.get("status", "healthy"),
                    "utilization": l.get("utilization", 0),
                    "latencyMs": l.get("latencyMs", 0),
                    "packetLoss": l.get("packetLoss", 0),
                }
            )
        services = [
            {**s, "status": s.get("status", "healthy"), "metrics": s.get("metrics", {})}
            for s in self.services.values()
        ]
        return {
            "site": self.raw["site"],
            "vantage": self.raw["vantage"],
            "nodes": nodes,
            "links": links,
            "services": services,
        }

    def get_device(self, device_id: str) -> dict | None:
        n = self.nodes.get(device_id)
        if not n:
            return None
        return {**n, "status": n.get("status", "healthy"), "metrics": n.get("metrics", {})}
