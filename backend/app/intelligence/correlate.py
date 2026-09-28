from .graph import TopologyGraph

WINDOW_S = 120


class Correlator:
    def __init__(self, graph: TopologyGraph):
        self.g = graph

    def related(self, a: str, b: str) -> bool:
        if a == b:
            return True
        if a in self.g.downstream(b) or b in self.g.downstream(a):
            return True
        if set(self.g.services_through(a)) & set(self.g.services_through(b)):
            return True
        try:
            return self.g.hop_distance(a, b) <= 3
        except Exception:
            return False

    def pick(self, entity: str, ts: float, open_incidents: list):
        best = None
        for inc in open_incidents:
            if ts - inc.last_activity > WINDOW_S:
                continue
            if any(self.related(entity, m) for m in inc.members):
                if best is None or inc.last_activity > best.last_activity:
                    best = inc
        return best
