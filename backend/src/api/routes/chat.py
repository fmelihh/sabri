from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket, Depends, Security

from models.user import User
from ..app import backend_app
from database.chat import create_chat_room
from chat.connection_manager import ConnectionManager
from authentication.dependencies import user_dependency, permission

chat_router = APIRouter()


@chat_router.websocket("/ws/chat")
async def ws_broadcast(
    channel_name: str, websocket: WebSocket, user: User = Depends(user_dependency)
):
    connection_manager = ConnectionManager()
    await connection_manager.connect(websocket, user, channel_name)
    while True:
        try:
            message = await websocket.receive_text()
            await connection_manager.broadcast(message)
        except WebSocketDisconnect:
            await connection_manager.disconnect(websocket, user, channel_name)
            return


@chat_router.post("/create")
async def create(
    chat_room_name: str,
    user: User = Security(
        permission, scopes=["admin:chat:create", "premium:chat:create"]
    ),
):
    await create_chat_room(room_name=chat_room_name, created_by=user.email)


backend_app.include_router(router=chat_router, prefix="/chat")
