from fastapi import FastAPI, Depends, HTTPException
from . import models
from .schemas import UserRegister, User, ResendEmail, UserLogin, Token
from .database import Base, engine, SessionLocal
from .utils import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import services
from uuid import UUID

app = FastAPI()

Base.metadata.create_all(bind=engine)
services.expired_emails_cleanup(SessionLocal())


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
