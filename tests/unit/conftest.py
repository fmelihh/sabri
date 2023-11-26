import pytest_asyncio
from loguru import logger
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from tests.unit.fixtures import *
from src.chat_app.models.user import User
from src.chat_app.models.chat_room import ChatRoom


@pytest_asyncio.fixture(autouse=True)
async def beanie_client():
    logger.info("Autoload beanie client fixture was triggered.")
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=[User, ChatRoom], database=client.get_database(name="db")
    )

    yield client

    logger.info("Beanie client tearing down.")
