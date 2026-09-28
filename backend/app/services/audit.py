from collections import deque
from datetime import datetime, timezone


class AuditLog:
    def __init__(self, maxlen: int = 200):
        self.entries: deque = deque(maxlen=maxlen)

    def log(self, actor: str, action: str, target: str, detail: dict | None = None):
        self.entries.appendleft(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "actor": actor,
                "action": action,
                "target": target,
                "detail": detail or {},
            }
        )

    def list(self) -> list[dict]:
        return list(self.entries)
