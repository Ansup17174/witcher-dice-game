from fastapi import APIRouter, Depends, HTTPException, Query
from ..database import get_db
from ..services import user_service
from ..models import UserModel
from ..schemas.users import (UserRegisterSchema, UserLoginSchema,
                             ResendEmailSchema, UserSchema, TokenSchema,
                             ChangePasswordSchema, ResetPasswordSchema,
                             UserStatsSchema)
from ..exceptions import auth_exception, get_unique_violation_exception
from ..config import password_context
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional


user_router = APIRouter(
    prefix="/auth",
    tags=['user'],
)


@user_router.post("/register")
def register(data: UserRegisterSchema, db: Session = Depends(get_db)):
    try:
        user_service.register_user(db=db, user_data=data)
        return {"detail": "Confirmation email sent"}
    except IntegrityError as exc:
        raise get_unique_violation_exception(exc)


@user_router.post("/resend-verification-email")
def resend(email_data: ResendEmailSchema, db: Session = Depends(get_db)):
    user_service.resend_verification_email(db=db, email=email_data.email)
    return {"detail": "Confirmation email sent"}


@user_router.post("/confirm-email/{user_id}/{token}")
def confirm_email(user_id: str, token: str, db: Session = Depends(get_db)):
    user_service.confirm_email(db=db, user_id=user_id, token=token)
    return {"detail": "Email confirmed successfully"}


@user_router.post("/change-password")
def change_password(
        data: ChangePasswordSchema,
        user: UserModel = Depends(user_service.authenticate_user),
        db: Session = Depends(get_db)
        ):
    if not password_context.verify(data.old_password, user.password):
        raise HTTPException(detail="Incorrect password", status_code=400)
    user_service.change_password(db=db, data=data, user=user)
    return {"detail": "Password changed!"}


@user_router.post("/reset-password")
def reset_password(data: ResetPasswordSchema, db: Session = Depends(get_db)):
    email_model = user_service.get_email(db=db, address=data.email, is_confirmed=True)
    if email_model is None:
        raise HTTPException(detail="Email not found", status_code=404)
    user_service.reset_password(db=db, email=email_model)
    return {"detail": "New password sent"}


@user_router.post("/login")
def login(data: UserLoginSchema, db: Session = Depends(get_db)):
    user = user_service.login_user(**data.dict(), db=db)
    if not user:
        raise auth_exception
    data = {"sub": user.username}
    token = user_service.generate_access_token(data=data)
    token = TokenSchema(access_token=token, token_type="Bearer")
    user_response = UserSchema.from_orm(user)
    return {**user_response.dict(), **token.dict()}


@user_router.get("/user", response_model=UserSchema)
def get_user(user: UserModel = Depends(user_service.authenticate_user)):
    return user


@user_router.get("/mystats", response_model=list[UserStatsSchema])
def get_user_stats(
        game: Optional[str] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        user: UserModel = Depends(user_service.authenticate_user),
        db: Session = Depends(get_db)
):
    limit = limit if limit >= 0 else 10
    offset = offset if offset >= 0 else 0
    if game is not None:
        user_stats = user_service.get_user_stats(db=db, user_id=user.id, game=game, limit=limit, offset=offset)
        return user_stats
    user_stats = user_service.get_user_stats(db=db, user_id=user.id, limit=limit, offset=offset)
    return user_stats
