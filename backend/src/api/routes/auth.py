from fastapi import APIRouter

from ..app import backend_app
from schemas.user import UserSchema
from schemas.auth import AuthSchema

auth_router = APIRouter()


@auth_router.post('/register')
async def register(user: UserSchema):
    pass


@auth_router.post("/login")
async def login(email: str, password: str) -> AuthSchema:
    pass


backend_app.include_router(router=auth_router, prefix="/auth")
