import pytest
import asyncio
import unittest.mock as mock
from fastapi.exceptions import HTTPException

from src.chat_app.database.user import set_new_user, get_user


@mock.patch("src.chat_app.database.user.User.find")
@pytest.mark.asyncio
async def test_set_new_user_with_exists_user(
    user_find_f: mock.MagicMock, user_object, user_schema
):
    future = asyncio.Future()
    future.set_result(True)
    user_find_f.return_value.exists.return_value = future

    with pytest.raises(HTTPException):
        await set_new_user(user_modal=user_schema)


@mock.patch("src.chat_app.database.user.get_password_hash")
@mock.patch("src.chat_app.database.user.User.insert")
@mock.patch("src.chat_app.database.user.User.find")
@pytest.mark.asyncio
async def test_set_new_user_with_not_exists_user(
    user_find_f: mock.MagicMock,
    user_insert_f: mock.MagicMock,
    password_hash_f: mock.MagicMock,
    user_object,
    user_schema,
):
    future = asyncio.Future()
    future.set_result(False)
    user_find_f.return_value.exists.return_value = future
    password_hash_f.return_value = "hashed password"
    user_insert_f.return_value = future
    await set_new_user(user_modal=user_schema)


@mock.patch("src.chat_app.database.user.User.find_one")
@pytest.mark.asyncio
async def test_get_user(user_find_one_f: mock.MagicMock, user_object):
    future = asyncio.Future()
    future.set_result(user_object)
    user_find_one_f.return_value = future
    await get_user(user_object.email)
