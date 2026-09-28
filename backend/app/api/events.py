from datetime import datetime, timezone, timedelta
from collections import deque
import time

from fastapi import APIRouter, Header, HTTPException, Request

from app.core.config import settings
from app.schemas.event import Event, EventBatch

router = APIRouter(tags=["events"])

# Simple in-memory rate limit: ≤ 50 req/s across events endpoints
_hits: deque[float] = deque(maxlen=200)


def _auth(token: str | None):
    if token != settings.ingest_token:
        raise HTTPException(status_code=401, detail="bad ingest token")


def _rate_limit():
    now = time.time()
    while _hits and now - _hits[0] > 1.0:
        _hits.popleft()
    if len(_hits) >= 50:
        raise HTTPException(status_code=429, detail="rate limit: max 50 events requests/sec")
    _hits.append(now)


def _check_ts(ev: Event):
    ts = ev.timestamp
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    skew = abs(datetime.now(timezone.utc) - ts)
    if skew > timedelta(minutes=5):
        raise HTTPException(status_code=422, detail="timestamp skew > 5 minutes")


@router.post("/events", status_code=202)
async def post_event(
    ev: Event, request: Request, x_rootiq_token: str | None = Header(None)
):
    _auth(x_rootiq_token)
    _rate_limit()
    _check_ts(ev)
    await request.app.state.pipeline.ingest(ev)
    return {"accepted": 1}


@router.post("/events/batch", status_code=202)
async def post_batch(
    batch: EventBatch, request: Request, x_rootiq_token: str | None = Header(None)
):
    _auth(x_rootiq_token)
    _rate_limit()
    for ev in batch.events:
        _check_ts(ev)
    for ev in batch.events:
        await request.app.state.pipeline.ingest(ev)
    return {"accepted": len(batch.events)}
