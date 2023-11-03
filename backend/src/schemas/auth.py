import datetime
from pydantic import BaseModel, Field


class AuthSchema(BaseModel):
    token: str
    expires_at: datetime.datetime
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
