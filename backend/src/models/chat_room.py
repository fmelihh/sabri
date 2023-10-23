from typing import List
from beanie import Document
from pydantic import Field, BaseModel

from .user import User


class ChatRoom(Document):
    name: str
    created_by: User
    max_capacity: int = Field(default=30)
