import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import models


async def initialize_mongo():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    await init_beanie(
        database=client.get_default_database(), document_models=models.__all__
    )
