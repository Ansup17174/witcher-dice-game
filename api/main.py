from fastapi import FastAPI, Depends, HTTPException
from .schemas import UserRegister, User, ResendEmail
from .database import Base, engine, SessionLocal
from .utils import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import services
from uuid import UUID

app = FastAPI()

Base.metadata.create_all(bind=engine)
services.expired_emails_cleanup(SessionLocal())


@app.get("/auth/users/{user_id}", response_model=User)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = services.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    return user


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
