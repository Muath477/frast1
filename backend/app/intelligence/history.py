import json
from pathlib import Path


class History:
    """Learns from resolved incidents: each confirmed root cause increases support."""

    def __init__(self, path: str = "data/history.json"):
        self.path = Path(path)
        self.counts: dict[str, int] = (
            json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        )

    def count(self, entity: str) -> int:
        return self.counts.get(entity, 0)

    def support(self, entity: str) -> float:
        n = self.count(entity)
        return n / (n + 1)

    def record(self, entity: str):
        self.counts[entity] = self.count(entity) + 1
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.counts, indent=2), encoding="utf-8")
