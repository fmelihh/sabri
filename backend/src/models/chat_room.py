from typing import List
from beanie import Document
from pydantic import Field, BaseModel

from .user import User


class ChatRoom(Document):
    name: str
    chat: list[str] = Field(default=[])
    users: list[User] = Field(default=[])
    max_capacity: int = Field(default=30)
