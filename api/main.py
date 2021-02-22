from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.user_router import user_router
from .routers.game_router import game_router
from .database import Base, engine, SessionLocal
from .services import user_service


app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)

app.include_router(user_router)
app.include_router(game_router)

Base.metadata.create_all(bind=engine)
user_service.expired_emails_cleanup(SessionLocal())
