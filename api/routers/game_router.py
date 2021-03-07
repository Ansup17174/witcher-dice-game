from fastapi import APIRouter, Depends, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from ..managers.general import OnlineUsersManager, PublicChatManager, RoomListManager
from ..managers.witcher import WitcherRoomManager
from ..services import user_service
from ..models import UserModel
from ..schemas.users import UserStatsSchema
from ..database import get_db
import asyncio
from sqlalchemy.orm import Session
from typing import Optional


game_router = APIRouter(
    prefix="/game",
    tags=['game']
)

online_users_manager = OnlineUsersManager()
public_chat_manager = PublicChatManager()
room_list_manager = RoomListManager()


@game_router.get("/ranking")
def get_ranking(
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        game: Optional[str] = None,
        db: Session = Depends(get_db)
):
    limit = limit if limit >= 0 else 10
    offset = offset if offset >= 0 else 0
    stats_models = user_service.get_user_stats(db=db, limit=limit, offset=offset, game=game)
    response_list = [{**UserStatsSchema.from_orm(stats).dict(), "username": stats.user.username}
                     for stats in stats_models]
    response_list.sort(key=lambda stats: stats['matches_won'], reverse=True)
    return response_list


@game_router.post("/create-room")
async def create_room(room_type: str, user: UserModel = Depends(user_service.authenticate_user)):
    room_types = {
        "Witcher-dice": WitcherRoomManager
    }
    if room_type not in room_types.keys():
        raise HTTPException(detail="Invalid room type", status_code=400)
    await room_list_manager.create_room(room_types[room_type])
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
            data = await ws.receive_json()
            await public_chat_manager.dispatch(data=data, ws=ws)
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


@game_router.websocket("/ws/room/{room_id}")
async def room_websocket(ws: WebSocket, room_id: str):
    selected_room = None
    for room in room_list_manager.room_list:
        if room.room_id == room_id and not room.game_state.is_finished:
            selected_room = room
            break
    if selected_room is None:
        raise WebSocketDisconnect
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            await selected_room.dispatch(data, ws)
    except WebSocketDisconnect:
        await selected_room.disconnect(ws)
