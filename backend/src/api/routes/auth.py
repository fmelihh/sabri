from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from ..app import backend_app
from schemas.user import UserSchema
from schemas.token import TokenSchema
from database.user import set_new_user
from authentication.dependencies import oauth_v2_dependency
from authentication.registry import retrieve_jwt_access_token

auth_router = APIRouter()


@auth_router.post("/register")
async def register(user: UserSchema):
    await set_new_user(user_modal=user)


@auth_router.post("/token", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token_schema = await retrieve_jwt_access_token(
        form_data.username, form_data.password
    )
    return token_schema


@auth_router.get("/me", response_model=UserSchema)
async def me(user: User = Depends(oauth_v2_dependency)):
    return UserSchema(**user.model_dump()).model_dump(exclude={"password"})


backend_app.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
