from fastapi import FastAPI, Depends, HTTPException
from .schemas import UserRegister, User
from .database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .services import register_user, get_user_by_id
from uuid import UUID

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/auth/users/{user_id}", response_model=User)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return get_user_by_id(db=db, user_id=user_id)


@app.post("/auth/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        register_user(db=db, user_data=data)
        return {"detail": "Confirmation email sent"}
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(detail=exc.orig.args[0], status_code=400)
