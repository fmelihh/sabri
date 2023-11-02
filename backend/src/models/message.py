import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    created_by: str
    message_text: str
    created_at: datetime = Field(default=datetime.datetime.now())
