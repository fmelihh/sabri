from pydantic import BaseModel, field_validator, ValidationError, EmailStr, Field


class UserSchema(BaseModel):
    age: int
    name: str
    nickname: str
    email: EmailStr
    family_name: str
    password: str | None = Field(default=None)

    @field_validator("age")
    @classmethod
    def check_age(cls, v: int):
        if 9 > v > 120:
            raise ValidationError("age must be between 9 and 120")
        return v
