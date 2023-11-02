from pydantic import BaseModel


class User(BaseModel):
    nickname: str
