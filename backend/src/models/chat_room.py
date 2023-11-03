from pydantic import Field
from beanie import Document

from schemas.message import MessageSchema


class ChatRoom(Document):
    name: str
    user_ids: list[str] = Field(default=[])
    chat: list[MessageSchema] = Field(default=[])
    max_capacity: int = Field(default=30)
