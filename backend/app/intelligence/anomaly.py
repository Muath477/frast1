"""Isolation Forest multivariate scorer — optional supporting evidence (Day 9)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

FEATURES = [
    "link-r1-sw1|link_utilization",
    "link-r1-sw1|link_latency_ms",
    "link-r1-sw1|link_packet_loss",
    "svc-web|http_latency_ms",
    "svc-dns|dns_latency_ms",
    "app01|cpu_percent",
]
MODEL = Path(__file__).resolve().parents[3] / "data" / "models" / "iforest.joblib"


def vectors_from_recording(path: str, step_s: float = 2.0) -> np.ndarray:
    last: dict[str, float] = {}
    rows: list[list[float]] = []
    t_next = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        key = f'{e["sourceId"]}|{e["metric"]}'
        last[key] = e["value"]
        t = e["ts"]
        if t_next is None:
            t_next = t + step_s
        if t >= t_next and all(f in last for f in FEATURES):
            rows.append([last[f] for f in FEATURES])
            t_next = t + step_s
    return np.array(rows) if rows else np.empty((0, len(FEATURES)))


def train(healthy_path: str) -> int:
    from sklearn.ensemble import IsolationForest
    import joblib

    X = vectors_from_recording(healthy_path)
    if len(X) < 10:
        raise ValueError("need at least 10 healthy vectors to train")
    m = IsolationForest(n_estimators=200, contamination=0.01, random_state=7).fit(X)
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(m, MODEL)
    return len(X)


class MultivariateScorer:
    def __init__(self):
        self.m = None
        if MODEL.exists():
            try:
                import joblib

                self.m = joblib.load(MODEL)
            except Exception:
                self.m = None

    def score(self, metrics: dict[str, dict[str, float]]) -> float | None:
        if not self.m:
            return None
        x = [metrics.get(f.split("|")[0], {}).get(f.split("|")[1], 0.0) for f in FEATURES]
        return float(np.clip(-self.m.decision_function([x])[0] * 4 + 0.5, 0, 1))
