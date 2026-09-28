from dataclasses import dataclass

from .baseline import Baseline
from .thresholds import static_severity


@dataclass
class Anomaly:
    entity_id: str
    metric: str
    value: float
    baseline: float
    severity: float
    first_seen: float
    last_seen: float


class Detector:
    def __init__(self):
        self.baseline = Baseline()
        self.active: dict[tuple[str, str], Anomaly] = {}
        self.alert_level: dict[tuple[str, str], float] = {}

    def observe(self, entity: str, metric: str, value: float, ts: float):
        """Returns (anomaly|None, raw_alert_level|None). Raw alert = new threshold crossing."""
        base, z = self.baseline.score(entity, metric, value)
        sev_static = static_severity(metric, value)
        sev_z = (
            min(1.0, max(0.0, (abs(z) - 3) / 3))
            if metric not in ("http_ok", "if_oper_status")
            else 0.0
        )
        # z amplifies only after a static threshold cross — prevents false incidents from tight EWMA
        sev = max(sev_static, sev_z) if sev_static >= 0.5 else 0.0
        key = (entity, metric)
        anomaly = None
        if sev >= 0.5:
            a = self.active.get(key)
            if a is None:
                a = self.active[key] = Anomaly(entity, metric, value, base, sev, ts, ts)
            a.value, a.severity, a.last_seen = value, max(a.severity, sev), ts
            anomaly = a
        elif key in self.active and ts - self.active[key].last_seen > 10:
            del self.active[key]
        self.baseline.learn(entity, metric, value, anomalous=sev >= 0.5)
        level = 1.0 if sev_static >= 1 else 0.5 if sev_static >= 0.5 else 0.0
        prev = self.alert_level.get(key, 0.0)
        self.alert_level[key] = level
        raw_alert = level if level > prev else None
        return anomaly, raw_alert
