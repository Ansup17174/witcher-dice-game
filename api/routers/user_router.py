from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from ..services import user_service
from ..models import UserModel
from ..schemas.users import (UserRegisterSchema, UserLoginSchema,
                             ResendEmailSchema, UserSchema, TokenSchema)
from ..exceptions import auth_exception
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID


user_router = APIRouter(
    prefix="/auth",
    tags=['user'],
    dependencies=[Depends(get_db), Depends(user_service.authenticate_user)]
)


@user_router.post("/register")
def register(data: UserRegisterSchema, db: Session):
    try:
        user_service.register_user(db=db, user_data=data)
        return {"detail": "Confirmation email sent"}
    except IntegrityError as exc:
        raise HTTPException(detail=exc.orig.args[0], status_code=400)


@user_router.post("/resend-verification-email")
def resend(email_data: ResendEmailSchema, db: Session):
    try:
        user_service.resend_verification_email(db=db, email=email_data.email)
        return {"detail": "Confirmation email sent"}
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(detail=exc.orig.args[0], status_code=400)


@user_router.get("/confirm-email/{user_id}/{token}")
def confirm_email(user_id: UUID, token: str, db: Session):
    user_service.confirm_email(db=db, user_id=user_id, token=token)
    return {"detail": "Email confirmed successfully"}


@user_router.post("/login")
def login(data: UserLoginSchema, db: Session):
    user = user_service.login_user(**data.dict(), db=db)
    if not user:
        raise auth_exception
    data = {"sub": user.username}
    token = user_service.generate_access_token(data=data)
    token = TokenSchema(access_token=token, token_type="Bearer")
    user_response = UserSchema.from_orm(user)
    return {**user_response.dict(), **token.dict()}


@user_router.get("user/", response_model=UserSchema)
def get_user(user: UserModel):
    return user
