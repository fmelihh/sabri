# import pika
# import threading
# from abc import ABC, abstractmethod
# from fastapi.websockets import WebSocket
#
# from models.user import User
# from .active_conn_dto import ActiveConnectionDto
#
#
# class SingletonChat(type):
#     _instance = None
#     _lock = threading.Lock()
#
#     def __call__(cls, *args, **kwargs):
#         if cls._instance is None:
#             with cls._lock:
#                 if cls._instance is None:
#                     cls._instance = super(SingletonChat, cls).__call__(*args, **kwargs)
#         return cls._instance
#
#
# class AbstractChat(ABC):
#
#     def __init__(self):
#         self._pika_conn = None
#         self._pika_channel = None
#         self._active_connections = None
#
#     def _remove_threads_from_closed_connection(self):
#         for active_connection in self.connections.values():
#             if active_connection.is_active is False:
#                 active_connection.current_thread.join()
#
#     def _set_active_connection(self, room_name: str, websocket: WebSocket):
#         if self.connections.get(room_name) is None:
#             t = threading.Thread(target=self.handle_message, args=[room_name])
#             self.connections[room_name] = ActiveConnectionDto(current_thread=t)
#             t.start()
#
#         self.connections[room_name].active_connections.append(websocket)
#
#     @property
#     def connections(self) -> dict[str, ActiveConnectionDto]:
#         if self._active_connections is None:
#             self._active_connections = dict()
#         return self._active_connections
#
#     @property
#     def pika_conn(self):
#         if self._pika_conn is None:
#             self._pika_conn = pika.BlockingConnection(
#                 pika.ConnectionParameters(host="localhost")
#             )
#         return self._pika_conn
#
#     @property
#     def pika_channel(self):
#         if self._pika_channel is None:
#             self._pika_channel = self.pika_conn.channel()
#         return self._pika_channel
#
#     @abstractmethod
#     def broadcast(self, message: str, room_name: str):
#         pass
#
#     @abstractmethod
#     def connect(self, websocket: WebSocket, user: User, room_name: str):
#         pass
#
#     @abstractmethod
#     def disconnect(self, websocket: WebSocket, user: User, room_name: str):
#         pass
#
#     @abstractmethod
#     def handle_message(self, room_name: str):
#         pass
#
#     def __del__(self):
#         self.pika_conn.close()
