import json
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings


class Recorder:
    def __init__(self):
        self.path: Path | None = None
        if settings.record_events:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
            root = Path(__file__).resolve().parents[3] / "data" / "recordings"
            root.mkdir(parents=True, exist_ok=True)
            self.path = root / f"{stamp}.jsonl"

    def write(self, ev) -> None:
        if not self.path:
            return
        line = {
            "ts": ev.timestamp.timestamp(),
            "sourceId": ev.source_id,
            "sourceType": ev.source_type,
            "metric": ev.metric,
            "value": ev.value,
            "unit": ev.unit,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line) + "\n")
