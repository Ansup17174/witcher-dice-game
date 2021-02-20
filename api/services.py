from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .schemas import UserRegister, Token
from uuid import uuid4, UUID
from . import config
from .models import User, Email, UserProfile
from .config import password_context
from .utils import send_confirmation_mail, get_db
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .exceptions import auth_exception


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def expired_emails_cleanup(db: Session):
    conditions = [Email.is_confirmed == False, Email.expiry_date <= datetime.now()]
    emails = db.query(Email).filter(and_(*conditions))
    users = [email.user for email in emails]
    for user in users:
        db.delete(user)
    db.commit()


def register_user(db: Session, user_data: UserRegister):
    hashed_password = password_context.hash(user_data.password)
    user_model = User(id=uuid4(), username=user_data.username, password=hashed_password)
    db.add(user_model)
    email_token = str(uuid4())
    expiry_date = datetime.now() + timedelta(days=1)
    email_model = Email(
        address=user_data.email,
        user_id=user_model.id,
        activation_token=email_token,
        expiry_date=expiry_date
    )
    db.add(email_model)
    userprofile_model = UserProfile(user_id=user_model.id)
    db.add(userprofile_model)
    db.commit()
    send_confirmation_mail(user_model)
    return user_model


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_active_user_by_username(db: Session, username: str):
    conditions = [Email.is_confirmed, User.username == username]
    return db.query(User).join(Email).filter(and_(*conditions)).first()


def get_email(db: Session, email: str):
    return db.query(Email).filter(Email.address == email).first()


def resend_verification_email(db: Session, email: str):
    email_model = db.query(Email).filter(and_(Email.address == email, Email.is_confirmed == False)).first()
    if email_model is None:
        raise HTTPException(detail="Email not found", status_code=404)
    user = get_user_by_id(db=db, user_id=email_model.user_id)
    email_model.activation_token = str(uuid4())
    db.commit()
    send_confirmation_mail(user=user)


def confirm_email(db: Session, user_id: UUID, token: str):
    conditions = [Email.is_confirmed == False, Email.activation_token == token, Email.user_id == user_id]
    email_model = db.query(Email).filter(and_(*conditions)).first()
    if email_model is None:
        raise HTTPException(detail="Invalid activation token", status_code=400)
    email_model.activation_token = ""
    email_model.is_confirmed = True
    db.commit()


def login_user(username: str, password: str, db: Session):
    user = get_user_by_username(username=username, db=db)
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
