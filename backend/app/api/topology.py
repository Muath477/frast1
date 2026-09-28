from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.services.topology_service import TopologyError

router = APIRouter(tags=["topology"])


class LayoutBody(BaseModel):
    positions: dict[str, dict[str, float]] = Field(default_factory=dict)


@router.get("/topology")
def get_topology(request: Request):
    return request.app.state.topology.snapshot()


@router.put("/topology/layout")
def put_layout(body: LayoutBody, request: Request):
    try:
        request.app.state.topology.save_layout(body.positions)
    except TopologyError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"ok": True}


@router.get("/devices/{device_id}")
def get_device(device_id: str, request: Request):
    device = request.app.state.topology.get_device(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail=f"unknown device: {device_id}")
    return device
