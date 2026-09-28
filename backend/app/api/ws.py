from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.hub import hub

router = APIRouter()


@router.websocket("/ws/operations")
async def operations(ws: WebSocket):
    await hub.connect(ws)
    await hub.send(ws, "snapshot", ws.app.state.snapshot())
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(ws)
