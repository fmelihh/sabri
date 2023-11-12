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


async def add_default_users():
    admin_user = User(
        age=25,
        name="Furkan Melih",
        email="admin@admin.com",
        password=get_password_hash("admin"),
        nickname="admin",
        family_name="Ercan",
        scopes=["admin"],
    )

    free_user = User(
        age=25,
        name="Furkan Melih",
        email="free_user@free.com",
        password=get_password_hash("free_user"),
        nickname="free_user",
        family_name="Ercan",
        scopes=[
            "free_user:user:read",
            "free_user:chat:read",
            "free_user:user:update",
            "free_user:user:delete",
            "free_user:user:create",
            "free_user:chat:update",
            "free_user:chat:delete",
            "free_user:chat:create",
        ],
    )

    premium_user = User(
        age=25,
        name="Furkan Melih",
        email="premium_user@premium.com",
        password=get_password_hash("premium_user"),
        nickname="premium_user",
        family_name="Ercan",
        scopes=[
            "premium:user:read",
            "premium:chat:read",
            "premium:user:update",
            "premium:user:delete",
            "premium:user:create",
            "premium:chat:update",
            "premium:chat:delete",
            "premium:chat:create",
        ],
    )

    for user in [admin_user, free_user, premium_user]:
        await User.find({User.email: user.email}).delete()
        await user.insert()
