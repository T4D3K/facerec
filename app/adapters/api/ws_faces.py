from fastapi import APIRouter, WebSocket

from app.core.factory import AppFactory

ws_router = APIRouter(prefix="/ws/v1")


@ws_router.websocket("/faces")
async def websocket_endpoint(websocket: WebSocket):
    cmd = AppFactory.get_ws_notification_cmd()
    await cmd.execute(websocket)
