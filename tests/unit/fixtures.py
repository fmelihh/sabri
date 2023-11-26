import pytest
import unittest.mock as mock
from beanie.odm.fields import PydanticObjectId

from src.chat_app.models.user import User
from src.chat_app.models.chat_room import ChatRoom
from src.chat_app.schemas.user import UserSchema


@pytest.fixture()
def user_object() -> mock.AsyncMock:
    user = User(
        **{
            "id": PydanticObjectId(),
            "age": 1,
            "name": "Test User",
            "email": "test@example.com",
            "password": "hashed password",
            "nickname": "test",
            "family_name": "test",
        }
    )
    return user


@pytest.fixture()
def empty_chat_room() -> ChatRoom:
    chat_room = ChatRoom(
        **{
            "name": "test empty chat room",
            "created_by": "test id",
            "max_capacity": 30,
            "user_ids": [],
            "chat": [],
        }
    )
    return chat_room


@pytest.fixture
def user_schema() -> UserSchema:
    user_schema = UserSchema(
        **{
            "age": 1,
            "name": "Test User",
            "email": "test@example.com",
            "password": "hashed password",
            "nickname": "test",
            "family_name": "test",
        }
    )
    return user_schema
