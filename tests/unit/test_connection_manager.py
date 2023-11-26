import pytest
import asyncio
import unittest.mock as mock
from src.chat_app.models.user import User
from src.chat_app.chat.connection_manager import ConnectionManager, Singleton


@pytest.fixture
def connection_manager() -> ConnectionManager:
    return ConnectionManager()


@mock.patch("src.chat_app.chat.connection_manager.add_user_to_chat_room")
@pytest.mark.asyncio
async def test_connection_manager_connect(
    add_user_to_chat_room_f: mock.MagicMock,
    connection_manager: ConnectionManager,
    user_object: User,
):
    connection_manager.active_connections = {}
    add_user_to_chat_room_future = asyncio.Future()
    add_user_to_chat_room_future.set_result(None)

    websocket_future = asyncio.Future()
    websocket_future.set_result(None)

    websocket_mock = mock.MagicMock()
    websocket_mock.accept.return_value = websocket_future

    add_user_to_chat_room_f.return_value = add_user_to_chat_room_future
    await connection_manager.connect(
        websocket=websocket_mock, user=user_object, room_name="test"
    )


@mock.patch("src.chat_app.chat.connection_manager.remove_user_from_chat_room")
@pytest.mark.asyncio
async def test_connection_manager_disconnect(
    remove_user_from_chat_room_f: mock.MagicMock,
    user_object: User,
    connection_manager: ConnectionManager,
):

    remove_user_from_chat_room_future = asyncio.Future()
    remove_user_from_chat_room_future.set_result(None)

    websocket_mock = mock.MagicMock()
    websocket_mock.return_value = "websocket value"

    remove_user_from_chat_room_f.return_value = remove_user_from_chat_room_future

    connection_manager.active_connections = {"test": [websocket_mock]}
    await connection_manager.disconnect(
        websocket=websocket_mock, user=user_object, room_name="test"
    )


@pytest.mark.asyncio
async def test_connection_manager_broadcast(connection_manager: ConnectionManager):
    websocket_future = asyncio.Future()
    websocket_future.set_result("websocket value")

    websocket_mock = mock.MagicMock()
    websocket_mock.send_text.return_value = websocket_future

    connection_manager.active_connections = {"test": [websocket_mock]}
    await connection_manager.broadcast(message="test message", room_name="test")


def test_singleton():
    class TestSingleton(metaclass=Singleton):
        def __init__(self, value: int):
            self.value = value

    instance1 = TestSingleton(1)
    instance2 = TestSingleton(2)

    assert instance1 is instance2
    assert instance1.value == 1
    assert instance2.value == 1
