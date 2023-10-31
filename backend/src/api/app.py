import fastapi
from config.mongo import initialize_mongo

backend_app: fastapi.FastAPI = fastapi.FastAPI()


@backend_app.on_event("startup")
async def startup():
    await initialize_mongo()


__all__ = ["backend_app"]
