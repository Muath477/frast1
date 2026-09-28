import json
from pathlib import Path

from app.intelligence.correlate import Correlator
from app.intelligence.graph import TopologyGraph


class _Inc:
    def __init__(self, members, last_activity):
        self.members = set(members)
        self.last_activity = last_activity


TOPO = json.loads(
    Path(__file__).resolve().parents[2].joinpath("configs/topology.json").read_text(encoding="utf-8")
)
g = TopologyGraph(TOPO)
c = Correlator(g)


def test_scenario1_symptoms_related():
    assert c.related("link-r1-sw1", "svc-web")
    assert c.related("link-r1-sw1", "svc-dns")
    assert c.related("svc-web", "svc-dns")


def test_distant_in_time_opens_new():
    open_inc = [_Inc({"link-r1-sw1"}, 0.0)]
    pick = c.pick("link-sw2-collector01", 200.0, open_inc)
    assert pick is None
