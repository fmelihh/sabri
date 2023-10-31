from models.user import User
from models.chat_room import ChatRoom
from fastapi.exceptions import WebSocketException


async def add_user_to_chat_room(chat_room_name: str, user: User):
    current_chat_room = await ChatRoom.find_one({"name": chat_room_name})
    if current_chat_room is None:
        raise WebSocketException(code=404, reason="Could not find chat room")

    await ChatRoom.find({"name": chat_room_name}).update({"$push": {"users": user.model_dump()}})



    # response = await ChatRoom.update({ChatRoom.name: chat_room_name}, {"$push": {ChatRoom.users: user}})

