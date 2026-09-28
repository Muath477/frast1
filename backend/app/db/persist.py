from datetime import datetime, timezone

from sqlalchemy import delete

from app.db.models import EvidenceRow, IncidentRow
from app.db.session import SessionLocal


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def upsert_incident(inc) -> None:
    blob = inc.to_dict()
    root = blob.get("rootCause") or {}
    with SessionLocal() as s:
        row = s.get(IncidentRow, blob["id"])
        if row is None:
            row = IncidentRow(id=blob["id"])
            s.add(row)
        row.title = blob["title"]
        row.status = blob["status"]
        row.severity = blob.get("severity") or "high"
        row.root_cause = root.get("entityId")
        row.confidence = root.get("confidence")
        row.opened_at = _parse_ts(blob["openedAt"]) or datetime.now(timezone.utc)
        row.resolved_at = _parse_ts(blob.get("resolvedAt"))
        row.snapshot = blob

        s.execute(delete(EvidenceRow).where(EvidenceRow.incident_id == blob["id"]))
        for ev in blob.get("evidence") or []:
            s.add(
                EvidenceRow(
                    incident_id=blob["id"],
                    entity_id=ev.get("entityId", ""),
                    metric=ev.get("metric", ""),
                    value=float(ev.get("value") or 0),
                    baseline=float(ev.get("baseline") or 0),
                    relation_type="symptom",
                    weight=float(ev.get("weight") or 0),
                    ts=_parse_ts(ev.get("ts")) or datetime.now(timezone.utc),
                )
            )
        s.commit()
