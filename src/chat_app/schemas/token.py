import datetime
from typing import Literal
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    expires_at: datetime.datetime
    token_type: Literal[
        "bearer",
    ] = Field(default="bearer")
    created_at: datetime.datetime = Field(default=datetime.datetime.now())


class TokenPayloadSchema(BaseModel):
    sub: str
