from fastapi import APIRouter, WebSocket
from ..app import backend_app

chat_router = APIRouter()


@chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(id(websocket))
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


backend_app.include_router(router=chat_router, prefix="/chat")
