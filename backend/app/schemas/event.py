from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import Field

from .common import CamelModel

SourceType = Literal["router", "switch", "server", "collector", "link", "service"]


class Event(CamelModel):
    event_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_id: str
    source_type: SourceType
    metric: str
    value: float
    unit: str
    interface: str | None = None
    severity: Literal["info", "warning", "critical"] = "info"
    metadata: dict[str, Any] = Field(default_factory=dict)


class EventBatch(CamelModel):
    events: list[Event] = Field(max_length=500)
