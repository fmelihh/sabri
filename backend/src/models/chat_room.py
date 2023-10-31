from typing import List
from beanie import Document
from pydantic import Field, BaseModel

from .user import User


class ChatRoom(Document):
    name: str
    chat: List[str] = Field(default=[])
    users: List[User] = Field(default=[])
    max_capacity: int = Field(default=30)
