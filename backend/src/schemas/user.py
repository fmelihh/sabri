from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    age: int
    name: str
    email: str
    password: str
    nickname: str
    family_name: str

