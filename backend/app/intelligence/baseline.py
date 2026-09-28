import math
from dataclasses import dataclass


@dataclass
class Stat:
    mean: float = 0.0
    var: float = 0.0
    n: int = 0


class Baseline:
    """EWMA per (entity, metric). Learning freezes during anomaly so it won't adapt to the fault."""

    def __init__(self, alpha: float = 0.05, warmup: int = 20):
        self.alpha = alpha
        self.warmup = warmup
        self.stats: dict[tuple[str, str], Stat] = {}

    def score(self, entity: str, metric: str, value: float) -> tuple[float, float]:
        """Returns (baseline_mean, z). z = 0 during warmup."""
        s = self.stats.setdefault((entity, metric), Stat(mean=value))
        if s.n < self.warmup:
            return s.mean, 0.0
        std = max(math.sqrt(s.var), 1e-3, 0.05 * abs(s.mean))
        return s.mean, (value - s.mean) / std

    def learn(self, entity: str, metric: str, value: float, anomalous: bool):
        s = self.stats.setdefault((entity, metric), Stat(mean=value))
        if anomalous:
            return
        d = value - s.mean
        s.mean += self.alpha * d
        s.var = (1 - self.alpha) * (s.var + self.alpha * d * d)
        s.n += 1
