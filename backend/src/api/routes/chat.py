from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from ..app import backend_app
from authentication.dependencies import oauth_v2_dependency

chat_router = APIRouter()


@chat_router.websocket("/ws/{channel_name}/{token}")
async def ws_broadcast(websocket: WebSocket, channel_name: str, token: str):
    user = await oauth_v2_dependency(token=token)
    await backend_app.chat_manager.connect(websocket, user, channel_name)
    while True:
        try:
            message = await websocket.receive_text()
            await backend_app.chat_manager.broadcast(message)
        except WebSocketDisconnect:
            await backend_app.chat_manager.disconnect(websocket, user, channel_name)
            return


backend_app.include_router(router=chat_router, prefix="/chat")
