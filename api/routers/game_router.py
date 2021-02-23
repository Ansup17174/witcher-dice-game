from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect
from ..websockets.managers import OnlineUsersManager, PublicChatManager, RoomListManager
from ..services import user_service
from ..models import UserModel
import asyncio

game_router = APIRouter(
    prefix="/game",
    tags=['game']
)

online_users_manager = OnlineUsersManager()
public_chat_manager = PublicChatManager()
room_list_manager = RoomListManager()


@game_router.post("/create-room")
async def create_room(user: UserModel = Depends(user_service.authenticate_user)):
    await room_list_manager.create_room()
    return {"detail": "Room created!"}


@game_router.websocket("/ws/online")
async def online_users(ws: WebSocket):
    await ws.accept()
    online_users_manager.connection_list.append([ws, ""])
    await online_users_manager.send_to_one(ws)
    try:
        while True:
            access_token = await ws.receive_text()
            await online_users_manager.authorize(ws, access_token=access_token)
    except WebSocketDisconnect:
        await online_users_manager.disconnect(ws)
        await online_users_manager.send_to_all()


@game_router.websocket("/ws/chat")
async def public_chat(ws: WebSocket):
    await ws.accept()
    public_chat_manager.connection_list.append([ws, ""])
    await public_chat_manager.send_chat_to_one(ws)
    try:
        while True:
            message = await ws.receive_text()
            await public_chat_manager.receive_message(message)
    except WebSocketDisconnect:
        await public_chat_manager.disconnect(ws)


@game_router.websocket("/ws/room-list")
async def room_list(ws: WebSocket):
    await ws.accept()
    room_list_manager.connection_list.append(ws)
    await room_list_manager.send_to_one(ws)
    try:
        while True:
            await asyncio.sleep(0)
    except WebSocketDisconnect:
        await room_list_manager.disconnect(ws)


@game_router.websocket("/ws/room/{room_id}/{access_token}")
async def room_websocket(ws: WebSocket, room_id: str, access_token: str):
    await ws.accept()
    selected_room = None
    for room in room_list_manager.room_list:
        if room.room_id == room_id and not room.game_state.is_finished:
            selected_room = room
            break
    if selected_room is None:
        raise WebSocketDisconnect
    await selected_room.authorize(ws, access_token)
    await selected_room.send_game_state()
    try:
        while True:
            data = await ws.receive_json()
            await selected_room.dispatch(data, ws)
    except WebSocketDisconnect:
        await selected_room.disconnect(ws)
