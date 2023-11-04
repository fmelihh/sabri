import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.user import User
from models.chat_room import ChatRoom


async def initialize_mongo():
    client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
    await init_beanie(database=client.db_name, document_models=[ChatRoom, User])
