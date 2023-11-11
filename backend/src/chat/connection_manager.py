from fastapi.websockets import WebSocket

from models.user import User
from database.chat import add_user_to_chat_room, remove_user_from_chat_room


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class ConnectionManager(metaclass=Singleton):
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, user: User, room_name: str):
        await add_user_to_chat_room(chat_room_name=room_name, user=user)
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket, user: User, room_name: str):
        await remove_user_from_chat_room(room_name, user)
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
