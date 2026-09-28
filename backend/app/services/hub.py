import json
import time

from fastapi import WebSocket


class Hub:
    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)

    def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)

    async def send(self, ws: WebSocket, type_: str, data):
        await ws.send_text(
            json.dumps({"type": type_, "ts": time.time(), "data": data}, default=str)
        )

    async def broadcast(self, type_: str, data):
        msg = json.dumps({"type": type_, "ts": time.time(), "data": data}, default=str)
        for c in list(self.clients):
            try:
                await c.send_text(msg)
            except Exception:
                self.clients.discard(c)


hub = Hub()
