# import threading
# from fastapi.websockets import WebSocket
# from pydantic import BaseModel, Field
#
#
# class ActiveConnectionDto(BaseModel):
#     current_thread: threading.Thread
#     is_active: bool = Field(default=True)
#     active_connections: list[WebSocket] = Field(default=[])
