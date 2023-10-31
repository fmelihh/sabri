from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: str
