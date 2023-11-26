import pytest
import asyncio
import unittest.mock as mock
from fastapi.exceptions import WebSocketException

from src.chat_app.models.user import User
from src.chat_app.models.chat_room import ChatRoom
from src.chat_app.database.chat import (
    add_user_to_chat_room,
    remove_user_from_chat_room,
    get_chat_room,
    create_chat_room,
)


@mock.patch("beanie.Document.update")
@mock.patch("src.chat_app.database.chat.get_chat_room")
@pytest.mark.asyncio
async def test_add_user_to_chat_with_empty_room(
    get_chat_room_f: mock.MagicMock,
    beanie_doc_update_f: mock.MagicMock,
    user_object: User,
    empty_chat_room: ChatRoom,
):
    beanie_doc_update_f.return_value = None
    get_chat_room_f.return_value = empty_chat_room
    await add_user_to_chat_room("test", user_object)


@mock.patch("src.chat_app.database.chat.get_chat_room")
@pytest.mark.asyncio
async def test_add_user_to_chat_with_full_room(
    get_chat_room_f: mock.MagicMock,
    user_object: User,
    empty_chat_room: ChatRoom,
):
    empty_chat_room.user_ids = ["some user"]
    empty_chat_room.max_capacity = 1

    get_chat_room_f.return_value = empty_chat_room
    with pytest.raises(WebSocketException):
        await add_user_to_chat_room("test", user_object)


@mock.patch("src.chat_app.database.chat.get_chat_room")
@pytest.mark.asyncio
async def test_add_user_to_chat_with_already_registered(
    get_chat_room_f: mock.MagicMock,
    user_object: User,
    empty_chat_room: ChatRoom,
):
    empty_chat_room.user_ids = [str(user_object.id)]
    get_chat_room_f.return_value = empty_chat_room
    res = await add_user_to_chat_room("test", user_object)
    assert res is None


@mock.patch("beanie.Document.update")
@mock.patch("src.chat_app.database.chat.get_chat_room")
@pytest.mark.asyncio
async def test_remove_user_from_chat_room(
    get_chat_room_f: mock.MagicMock,
    beanie_doc_update_f: mock.MagicMock,
    user_object: User,
    empty_chat_room: ChatRoom,
):
    beanie_doc_update_f.return_value = None
    get_chat_room_f.return_value = empty_chat_room
    await remove_user_from_chat_room("test", user_object)


@mock.patch("beanie.Document.find_one")
@pytest.mark.asyncio
async def test_get_chat_room_returns_chat_room(
    find_one_doc_update_f: mock.Mock,
    user_object: User,
    empty_chat_room: ChatRoom,
):
    future = asyncio.Future()
    future.set_result(empty_chat_room)
    find_one_doc_update_f.return_value = future
    chat_room = await get_chat_room("test")
    assert chat_room == empty_chat_room


@mock.patch("beanie.Document.find_one")
@pytest.mark.asyncio
async def test_get_chat_room_returns_none(
    find_one_doc_update_f: mock.Mock,
    user_object: User,
    empty_chat_room: ChatRoom,
):
    future = asyncio.Future()
    future.set_result(None)
    find_one_doc_update_f.return_value = future
    with pytest.raises(WebSocketException):
        await get_chat_room("test")


@mock.patch("beanie.Document.delete")
@mock.patch("beanie.Document.insert")
@mock.patch("src.chat_app.database.chat.ChatRoom.find")
@mock.patch("src.chat_app.database.chat.ChatRoom")
@pytest.mark.asyncio
async def test_create_chat_room(
    mock_chat_room: mock.MagicMock,
    beanie_doc_find_f: mock.MagicMock,
    beanie_doc_insert_f: mock.MagicMock,
    beanie_doc_delete_f: mock.MagicMock,
    user_object: User,
    empty_chat_room: ChatRoom,
):

    find_future = asyncio.Future()
    find_future.set_result(empty_chat_room)

    delete_future = asyncio.Future()
    delete_future.set_result(None)

    insert_future = asyncio.Future()
    insert_future.set_result(None)

    mock_chat_room.return_value = empty_chat_room
    beanie_doc_find_f.return_value = empty_chat_room
    beanie_doc_delete_f.return_value = delete_future
    beanie_doc_insert_f.return_value = insert_future
    await create_chat_room(empty_chat_room.name, str(user_object.id))
