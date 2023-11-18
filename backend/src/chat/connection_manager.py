import threading
from fastapi.websockets import WebSocket

from models.user import User
from database.chat import add_user_to_chat_room, remove_user_from_chat_room


class Singleton(type):
    _instance = None
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class ConnectionManager(metaclass=Singleton):
    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user: User, room_name: str):
        await add_user_to_chat_room(chat_room_name=room_name, user=user)
        await websocket.accept()

        if self.active_connections.get(room_name) is None:
            self.active_connections[room_name] = set()

        self.active_connections[room_name].add(websocket)

    async def disconnect(self, websocket: WebSocket, user: User, room_name: str):
        await remove_user_from_chat_room(room_name, user)
        self.active_connections[room_name].remove(websocket)

    async def broadcast(self, message: str, room_name: str):
        for connection in self.active_connections[room_name]:
            await connection.send_text(message)
