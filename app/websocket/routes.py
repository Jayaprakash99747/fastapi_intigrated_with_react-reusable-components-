from fastapi import APIRouter, WebSocket
from app.websocket.notification import manager

router = APIRouter()


@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):
    await manager.connect(websocket, "admin")

    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket, "admin")


@router.websocket("/ws/user")
async def user_ws(websocket: WebSocket):
    await manager.connect(websocket, "user")

    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket, "user")