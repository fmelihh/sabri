import datetime
from pydantic import Field
from beanie import Document


class User(Document):
    age: int
    name: str
    email: str
    password: str
    nickname: str
    family_name: str
    trust_score: int = Field(default=0)
    registered_channels: list[str] = Field(default=[])
    updated_at: datetime.datetime | None = Field(default=None)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
