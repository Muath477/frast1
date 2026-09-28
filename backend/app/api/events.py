from fastapi import APIRouter, Header, HTTPException, Request

from app.core.config import settings
from app.schemas.event import Event, EventBatch

router = APIRouter(tags=["events"])


def _auth(token: str | None):
    if token != settings.ingest_token:
        raise HTTPException(status_code=401, detail="bad ingest token")


@router.post("/events", status_code=202)
async def post_event(
    ev: Event, request: Request, x_rootiq_token: str | None = Header(None)
):
    _auth(x_rootiq_token)
    await request.app.state.pipeline.ingest(ev)
    return {"accepted": 1}


@router.post("/events/batch", status_code=202)
async def post_batch(
    batch: EventBatch, request: Request, x_rootiq_token: str | None = Header(None)
):
    _auth(x_rootiq_token)
    for ev in batch.events:
        await request.app.state.pipeline.ingest(ev)
    return {"accepted": len(batch.events)}
