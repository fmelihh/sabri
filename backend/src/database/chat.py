from models.user import User
from models.chat_room import ChatRoom
from fastapi.exceptions import WebSocketException


async def add_user_to_chat_room(chat_room_name: str, user: User):
    user_id = str(user.id)
    chat_room = await get_chat_room(room_name=chat_room_name)
    if user_id in chat_room.user_ids:
        return
    if len(chat_room.user_ids) + 1 > chat_room.max_capacity:
        raise WebSocketException(code=500, reason="chat room capacity is full")

    await chat_room.update({"$push": {"user_ids": user_id}})


async def remove_user_from_chat_room(chat_room_name: str, user: User):
    chat_room = await get_chat_room(room_name=chat_room_name)
    await chat_room.update({"$pull": {"user_ids": str(user.id)}})


async def get_chat_room(room_name: str) -> ChatRoom:
    current_chat_room = await ChatRoom.find_one({"name": room_name})
    if current_chat_room is None:
        raise WebSocketException(code=404, reason="could not find chat room")

    return current_chat_room


async def create_chat_room(room_name: str, created_by: str):
    chat_room = ChatRoom(name=room_name, created_by=created_by)
    await ChatRoom.find({ChatRoom.name: room_name}).delete()
    await chat_room.insert()


async def create_default_chat_room():
    await create_chat_room(room_name="alpha", created_by="admin@admin.com")
