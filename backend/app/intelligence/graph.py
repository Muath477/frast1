import networkx as nx


class TopologyGraph:
    """Devices and links are graph nodes; links are intermediate so link ids appear in paths."""

    def __init__(self, topo: dict):
        self.g = nx.Graph()
        self.vantage = topo["vantage"]
        for n in topo["nodes"]:
            self.g.add_node(n["id"], kind="device", label=n["label"])
        for l in topo["links"]:
            self.g.add_node(
                l["id"],
                kind="link",
                label=f'{l["source"].upper()} {l["sourcePort"]} → {l["target"].upper()} {l["targetPort"]}',
            )
            self.g.add_edge(l["source"], l["id"])
            self.g.add_edge(l["id"], l["target"])
        self.services = {s["id"]: s for s in topo["services"]}
        for s in self.services.values():
            self.g.add_node(s["id"], kind="service", label=s["label"])
        self._paths = {sid: self._path(sid) for sid in self.services}

    def _path(self, sid: str) -> list[str]:
        s = self.services[sid]
        chain = nx.shortest_path(self.g, self.vantage, s["host"])
        deps: list[str] = []
        for d in s.get("dependsOn", []):
            for x in self._path(d):
                if x not in chain and x not in deps:
                    deps.append(x)
        return chain + deps + [sid]

    def service_dependencies(self, sid: str) -> list[str]:
        return self._paths[sid]

    def downstream(self, x: str) -> set[str]:
        out: set[str] = set()
        for p in self._paths.values():
            if x in p:
                out |= set(p[p.index(x) + 1 :])
        return out

    def upstream(self, x: str) -> set[str]:
        out: set[str] = set()
        for p in self._paths.values():
            if x in p:
                out |= set(p[: p.index(x)])
        return out

    def services_through(self, x: str) -> list[str]:
        return [sid for sid, p in self._paths.items() if x in p]

    def label(self, x: str) -> str:
        return self.g.nodes[x]["label"]

    def hop_distance(self, a: str, b: str) -> int:
        if a in self.services or b in self.services:
            return 0 if (a in self.downstream(b) or b in self.downstream(a) or a == b) else 99
        return nx.shortest_path_length(self.g, a, b)
