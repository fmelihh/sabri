import fastapi
from config.mongo import initialize_mongo
from database.chat import create_default_chat_room

backend_app: fastapi.FastAPI = fastapi.FastAPI()


@backend_app.on_event("startup")
async def startup():
    await initialize_mongo()
    await create_default_chat_room()


__all__ = ["backend_app"]
