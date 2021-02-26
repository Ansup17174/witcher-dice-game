from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..schemas.users import UserRegisterSchema, ChangePasswordSchema
from uuid import uuid4, UUID
from .. import config
from ..models import UserModel, EmailModel, UserProfileModel
from ..database import get_db
from ..config import password_context
from ..utils import send_confirmation_mail, send_new_password
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from ..exceptions import auth_exception
import string
import random


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def expired_emails_cleanup(db: Session):
    conditions = [EmailModel.is_confirmed == False, EmailModel.expiry_date <= datetime.now()]
    emails = db.query(EmailModel).filter(and_(*conditions))
    users = [email.user for email in emails]
    for user in users:
        db.delete(user)
    db.commit()


def register_user(db: Session, user_data: UserRegisterSchema):
    hashed_password = password_context.hash(user_data.password1)
    user_model = UserModel(id=uuid4(), username=user_data.username, password=hashed_password)
    db.add(user_model)
    email_token = str(uuid4())
    expiry_date = datetime.now() + timedelta(days=1)
    email_model = EmailModel(
        address=user_data.email,
        user_id=user_model.id,
        activation_token=email_token,
        expiry_date=expiry_date
    )
    db.add(email_model)
    userprofile_model = UserProfileModel(user_id=user_model.id)
    db.add(userprofile_model)
    db.commit()
    send_confirmation_mail(user_model)
    return user_model


def get_users(db: Session, **kwargs):
    conditions = [getattr(UserModel, key) == value for key, value in kwargs.items()]
    return db.query(UserModel).filter(and_(*conditions))


def get_user(db: Session, **kwargs):
    return get_users(db, **kwargs).first()


def get_active_user_by_username(db: Session, username: str):
    conditions = [EmailModel.is_confirmed, UserModel.username == username]
    return db.query(UserModel).join(EmailModel).filter(and_(*conditions)).first()


def get_emails(db: Session, **kwargs):
    conditions = [getattr(EmailModel, key) == value for key, value in kwargs.items()]
    return db.query(EmailModel).filter(and_(*conditions))


def get_email(db: Session, **kwargs):
    return get_emails(db, **kwargs).first()


def get_user_profiles(db: Session, **kwargs):
    conditions = [getattr(UserProfileModel, key) == value for key, value in kwargs.items()]
    return db.query(UserProfileModel).filter(and_(*conditions))


def get_user_profile(db: Session, **kwargs):
    return get_user_profiles(db, **kwargs).first()


def resend_verification_email(db: Session, email: str):
    email_model = get_email(db=db, address=email, is_confirmed=False)
    if email_model is None:
        raise HTTPException(detail="Email not found", status_code=404)
    user = get_user(db=db, id=email_model.user_id)
    email_model.activation_token = str(uuid4())
    db.commit()
    send_confirmation_mail(user=user)


def confirm_email(db: Session, user_id: UUID, token: str):
    conditions = [
        EmailModel.is_confirmed == False,
        EmailModel.activation_token == token,
        EmailModel.user_id == user_id
    ]
    email_model = db.query(EmailModel).filter(and_(*conditions)).first()
    if email_model is None:
        raise HTTPException(detail="Invalid activation token", status_code=400)
    email_model.activation_token = ""
    email_model.is_confirmed = True
    db.commit()


def change_password(db: Session, data: ChangePasswordSchema, user: UserModel):
    user.password = password_context.hash(data.new_password1)
    db.commit()


def login_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    if not user:
        return None
    if not user.email.is_confirmed:
        return None
    if not password_context.verify(password, user.password):
        return None
    return user


def authenticate_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        data = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM])
        expire_time = datetime.utcfromtimestamp(data.get('exp'))
        if datetime.utcnow() > expire_time:
            raise auth_exception
        username = data.get('sub')
        user = get_active_user_by_username(db=db, username=username)
        if not user:
            raise auth_exception
        return user
    except JWTError:
        raise HTTPException(detail="Invalid access token", status_code=401)


def generate_access_token(
        data: dict,
        expire_delta: Optional[timedelta] = timedelta(minutes=30)
):
    to_encode = {**data, 'exp': datetime.utcnow() + expire_delta}
    return jwt.encode(to_encode, key=config.SECRET_KEY, algorithm=config.ALGORITHM)


def reset_password(db: Session, email: EmailModel):
    user_model = get_user(db=db, id=email.user_id)
    password = ""
    for i in range(20):
        password += random.choice(string.ascii_letters + string.digits)
    user_model.password = password_context.hash(password)
    send_new_password(user=user_model, password=password)
    db.commit()
