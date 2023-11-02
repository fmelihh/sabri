from models.user import User
from models.chat_room import ChatRoom
from fastapi.exceptions import WebSocketException


async def add_user_to_chat_room(chat_room_name: str, user: User):
    current_chat_room = await ChatRoom.find_one({"name": chat_room_name})
    if current_chat_room is None:
        raise WebSocketException(code=404, reason="could not find chat room")

    if len(current_chat_room.users) + 1 > current_chat_room.max_capacity:
        raise WebSocketException(code=500, reason="chat room capacity is full")

    await ChatRoom.find({"name": chat_room_name}).update({"$push": {"users": user.model_dump()}})


async def create_default_chat_room():
    default = ChatRoom(name="alpha")
    await ChatRoom.find({ChatRoom.name: default.name}).delete()
    await default.insert()

