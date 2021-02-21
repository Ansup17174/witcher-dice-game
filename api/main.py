from fastapi import FastAPI, Depends, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .websockets import OnlineUsersManager, PublicChatManager, RoomListManager, RoomManager
from . import models
from .schemas import UserRegister, User, ResendEmail, UserLogin, Token
from .database import Base, engine, SessionLocal
from .utils import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import services
from uuid import UUID, uuid4
import asyncio
import json

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)


Base.metadata.create_all(bind=engine)
services.expired_emails_cleanup(SessionLocal())

online_users_manager = OnlineUsersManager()
public_chat_manager = PublicChatManager()
room_list_manager = RoomListManager()



@app.post("/auth/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        services.register_user(db=db, user_data=data)
        return {"detail": "Confirmation email sent"}
    except IntegrityError as exc:
        raise HTTPException(detail=exc.orig.args[0], status_code=400)


@app.post("/auth/resend-verification-email")
def resend(email_data: ResendEmail, db: Session = Depends(get_db)):
    try:
        services.resend_verification_email(db=db, email=email_data.email)
        return {"detail": "Confirmation email sent"}
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(detail=exc.orig.args[0], status_code=400)


@app.get("/auth/confirm-email/{user_id}/{token}")
def confirm_email(user_id: UUID, token: str, db: Session = Depends(get_db)):
    services.confirm_email(db=db, user_id=user_id, token=token)
    return {"detail": "Email confirmed successfully"}


@app.post("/auth/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = services.login_user(**data.dict(), db=db)
    if not user:
        raise HTTPException(detail="Unable to login with given credentials", status_code=400)
    data = {"sub": user.username}
    token = services.generate_access_token(data=data)
    token_model = Token(access_token=token, token_type="Bearer")
    user_response = User.from_orm(user)
    return {**user_response.dict(), **token_model.dict()}


@app.get("/auth/user/", response_model=User)
def get_user(user: models.User = Depends(services.authenticate_user)):
    return user


@app.post("/create-room")
async def create_room(user: models.User = Depends(services.authenticate_user)):
    await room_list_manager.create_room()
    return {"detail": "Room created!"}

# @app.post("/send-invite/{username}")
# def invite(username: str,
#            user: models.User = Depends(services.authenticate_user),
#            db: Session = Depends(get_db)
#            ):
#     invited_user = services.get_active_user_by_username(db=db, username=username)
#     if not invited_user:
#         raise HTTPException(detail="User not found", status_code=404)
#     game_id = str(uuid4())
#     game = GameManager(game_id)
#     games_list.append(game)


@app.websocket("/ws/online")
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


@app.websocket("/ws/chat")
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


@app.websocket("/ws/room-list")
async def room_list(ws: WebSocket):
    await ws.accept()
    room_list_manager.connection_list.append(ws)
    await room_list_manager.send_to_one(ws)
    try:
        while True:
            await asyncio.sleep(0)
    except WebSocketDisconnect:
        room_list_manager.connection_list.remove(ws)
        await ws.close()


@app.websocket("/ws/{room_id}/{access_token}")
async def room_websocket(ws: WebSocket, room_id: str, access_token: str):
    await ws.accept()
    selected_room = None
    for room in room_list_manager.room_list:
        if room.room_id == room_id:
            selected_room = room
            break
    if not selected_room:
        await ws.close()
    await selected_room.authorize(ws, access_token)
    await selected_room.send_game_state()
    try:
        while True:
            game_state = await ws.receive_json()

    except WebSocketDisconnect:
        await selected_room.disconnect(ws)
