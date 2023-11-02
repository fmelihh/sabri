from pydantic import Field
from beanie import Document

from .user import User
from .message import Message


class ChatRoom(Document):
    name: str
    users: list[User] = Field(default=[])
    chat: list[Message] = Field(default=[])
    max_capacity: int = Field(default=30)
