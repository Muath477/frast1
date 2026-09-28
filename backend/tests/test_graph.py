import json
from pathlib import Path

from app.intelligence.graph import TopologyGraph

TOPO = json.loads(
    Path(__file__).resolve().parents[2].joinpath("configs/topology.json").read_text(encoding="utf-8")
)
g = TopologyGraph(TOPO)


def test_web_path_crosses_uplink_and_dns():
    p = g.service_dependencies("svc-web")
    assert p[0] == "collector01" and p[-1] == "svc-web"
    assert "link-r1-sw1" in p and "svc-dns" in p


def test_dns_is_downstream_of_uplink():
    assert {"svc-dns", "svc-web", "app01"} <= g.downstream("link-r1-sw1")


def test_uplink_is_upstream_of_dns():
    assert "link-r1-sw1" in g.upstream("svc-dns")


def test_collector_access_link_not_downstream_of_uplink():
    assert "link-sw2-collector01" not in g.downstream("link-r1-sw1")
