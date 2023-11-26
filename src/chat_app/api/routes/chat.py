from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket, Security

from ..app import backend_app
from ...models.user import User
from ...database.chat import create_chat_room
from ...chat.connection_manager import ConnectionManager
from ...authentication.dependencies import user_dependency, token_dependency, permission

chat_router = APIRouter()


@chat_router.websocket("/ws/chat")
async def ws_broadcast(channel_name: str, websocket: WebSocket):
    token_payload = await token_dependency(token=websocket.headers["authorization"])
    user = await user_dependency(token_payload=token_payload)

    connection_manager = ConnectionManager()
    await connection_manager.connect(websocket, user, channel_name)
    while True:
        try:
            message = await websocket.receive_text()
            await connection_manager.broadcast(message, channel_name)
        except WebSocketDisconnect:
            await connection_manager.disconnect(websocket, user, channel_name)
            return


@chat_router.post("/create/admin/chat")
async def create_admin_chat(
    chat_room_name: str,
    user: User = Security(permission, scopes=["admin:chat:create"]),
):
    await create_chat_room(room_name=chat_room_name, created_by=user.email)


@chat_router.post("/create/premium/chat")
async def create_premium_chat(
    chat_room_name: str,
    user: User = Security(permission, scopes=["premium:chat:create"]),
):
    await create_chat_room(room_name=chat_room_name, created_by=user.email)


backend_app.include_router(router=chat_router, prefix="/chat")
