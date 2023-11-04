from fastapi import APIRouter, WebSocket

from models.user import User
from database.chat import add_user_to_chat_room
from ..app import backend_app

chat_router = APIRouter()


@chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_name: str, email: str):
    print(id(websocket))
    await add_user_to_chat_room(
        chat_room_name="test", user=User(name=user_name, email=email)
    )
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


backend_app.include_router(router=chat_router, prefix="/chat")
