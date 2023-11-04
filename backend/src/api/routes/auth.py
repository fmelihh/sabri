from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..app import backend_app
from schemas.user import UserSchema
from schemas.token import TokenSchema
from database.user import register_user

auth_router = APIRouter()


@auth_router.post("/register")
async def register(user: UserSchema):
    await register_user(user_modal=user)
    return True

@auth_router.post("/token", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)


backend_app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
