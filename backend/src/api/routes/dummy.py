from fastapi import APIRouter

from ..app import backend_app

dummy_router = APIRouter()


@dummy_router.get("/hello")
def hello():
    return "Hello"


backend_app.include_router(router=dummy_router, prefix="/dummy")
