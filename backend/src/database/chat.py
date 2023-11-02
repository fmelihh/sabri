from models.user import User
from models.chat_room import ChatRoom
from fastapi.exceptions import WebSocketException


async def add_user_to_chat_room(chat_room_name: str, user: User):
    chat_room = await get_chat_room(room_name=chat_room_name)
    if len(chat_room.users) + 1 > chat_room.max_capacity:
        raise WebSocketException(code=500, reason="chat room capacity is full")

    await chat_room.update({"$push": {"users": user.model_dump()}})


async def remove_user_from_chat_room(chat_room_name: str, user: User):
    chat_room = await get_chat_room(room_name=chat_room_name)
    await chat_room.update({"$pull": {"users": user.model_dump()}})


async def get_chat_room(room_name: str) -> ChatRoom:
    current_chat_room = await ChatRoom.find_one({"name": room_name})
    if current_chat_room is None:
        raise WebSocketException(code=404, reason="could not find chat room")

    return current_chat_room


async def create_default_chat_room():
    default = ChatRoom(name="alpha")
    await ChatRoom.find({ChatRoom.name: default.name}).delete()
    await default.insert()

