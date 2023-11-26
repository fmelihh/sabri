from pydantic import Field
from beanie import Document

from ..schemas.message import MessageSchema


class ChatRoom(Document):
    name: str
    created_by: str
    max_capacity: int = Field(default=30)
    user_ids: list[str] = Field(default=[])
    chat: list[MessageSchema] = Field(default=[])

