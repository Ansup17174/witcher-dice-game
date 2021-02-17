from fastapi import FastAPI, Depends, HTTPException
from .schemas import UserRegister, User
from .database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .services import register_user

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/register", response_model=User)
async def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        registered_user = register_user(db=db, user_data=data)
        return registered_user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(detail=exc.orig.args[0], status_code=400)
