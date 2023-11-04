from fastapi import HTTPException

from models.user import User
from schemas.user import UserSchema
from utils.hash import get_password_hash


async def set_new_user(user_modal: UserSchema):
    is_exists = await User.find({User.email: user_modal.email}).exists()
    if is_exists:
        raise HTTPException(status_code=500, detail="user already registered")
    user_modal.password = get_password_hash(user_modal.password)
    await User(**user_modal.model_dump()).insert()


async def get_user(email: str) -> User | None:
    user = await User.find_one({User.email: email})
    return user
