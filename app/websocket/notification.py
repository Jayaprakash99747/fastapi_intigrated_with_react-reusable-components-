from fastapi import WebSocket
from typing import List, Dict


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "admin": [],
            "user": []
        }

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        self.active_connections[channel].append(websocket)

    def disconnect(self, websocket: WebSocket, channel: str):
        self.active_connections[channel].remove(websocket)

    async def send_to_channel(self, channel: str, message: dict):
        for connection in self.active_connections.get(channel, []):
            await connection.send_json(message)


manager = ConnectionManager()