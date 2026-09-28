from dataclasses import dataclass, field
from math import exp

from .graph import TopologyGraph

WEIGHTS = {
    "metric_anomaly": 0.30,
    "dependency_overlap": 0.25,
    "temporal_proximity": 0.20,
    "blast_radius": 0.15,
    "historical_support": 0.10,
}
SUPPRESSION = 0.5
LOW_CONFIDENCE = 0.55


@dataclass
class Candidate:
    entity_id: str
    label: str
    score: float
    components: dict[str, float]
    evidence: list[str] = field(default_factory=list)
    suppressed_by: str | None = None

    def to_dict(self) -> dict:
        return {
            "entityId": self.entity_id,
            "label": self.label,
            "score": self.score,
            "components": self.components,
            "evidence": self.evidence,
            "suppressedBy": self.suppressed_by,
        }


def fmt(a) -> str:
    unit = {
        "link_utilization": "%",
        "link_packet_loss": "%",
        "dns_success_rate": "%",
        "cpu_percent": "%",
        "mem_percent": "%",
    }.get(a.metric, " ms" if a.metric.endswith("_ms") else "")
    return f"{a.metric} = {a.value:.1f}{unit} (baseline {a.baseline:.1f}{unit})"


def rank(anomalies: list, affected_services: list[str], g: TopologyGraph, history) -> tuple[list[Candidate], float]:
    by_entity: dict[str, list] = {}
    for a in anomalies:
        by_entity.setdefault(a.entity_id, []).append(a)
    if not by_entity:
        return [], 0.0
    t0 = min(a.first_seen for a in anomalies)
    anomalous = set(by_entity)
    paths = [set(g.service_dependencies(s)) for s in affected_services]
    out: list[Candidate] = []
    for c, own in by_entity.items():
        first = min(a.first_seen for a in own)
        comps = {
            "metric_anomaly": max(a.severity for a in own),
            "dependency_overlap": (sum(1 for p in paths if c in p) / len(paths)) if paths else 0.0,
            "temporal_proximity": exp(-(first - t0) / 30.0),
            "blast_radius": len(anomalous & g.downstream(c)) / max(1, len(anomalous - {c})),
            "historical_support": history.support(c),
        }
        score = sum(WEIGHTS[k] * v for k, v in comps.items())
        upstream_bad = sorted(anomalous & g.upstream(c))
        suppressed_by = upstream_bad[0] if upstream_bad else None
        if suppressed_by:
            score *= SUPPRESSION
        ev = [fmt(a) + f" at +{a.first_seen - t0:.0f}s" for a in sorted(own, key=lambda x: -x.severity)]
        if comps["dependency_overlap"] > 0:
            ev.append(
                f"{sum(1 for p in paths if c in p)}/{len(paths)} affected services depend on this element"
            )
        if comps["historical_support"] > 0:
            ev.append(f"Matches {history.count(c)} previously resolved incident(s)")
        out.append(
            Candidate(
                c,
                g.label(c),
                round(score, 3),
                {k: round(v, 3) for k, v in comps.items()},
                ev,
                suppressed_by,
            )
        )
    out.sort(key=lambda x: x.score, reverse=True)
    top = out[:3]
    s1 = top[0].score
    s2 = top[1].score if len(top) > 1 else 0.0
    confidence = max(0.0, min(0.99, s1 - max(0.0, 0.15 - (s1 - s2))))
    return top, round(confidence, 2)
