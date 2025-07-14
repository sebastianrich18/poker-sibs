from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
from ..domain.entities import JoinAck, ErrorMessage

app = FastAPI(title="Lobby")

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active.pop(user_id, None)

    async def broadcast(self, message: dict):
        for ws in list(self.active.values()):
            await ws.send_json(message)

manager = ConnectionManager()

@app.websocket("/lobby/{lobby_id}/ws")
async def websocket_endpoint(websocket: WebSocket, lobby_id: str, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        await websocket.send_json(JoinAck(userId=user_id, seat=len(manager.active)).dict())
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast({"userId": user_id, "event": "left"})
