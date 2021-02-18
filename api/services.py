from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .schemas import UserRegister
from uuid import uuid4, UUID
from .models import User, Email
from .config import password_context
from .utils import send_confirmation_mail
from datetime import datetime, timedelta


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
    expiry_date = datetime.now() + timedelta(seconds=30)
    email_model = Email(
        address=user_data.email,
        user_id=user_model.id,
        activation_token=email_token,
        expiry_date=expiry_date
    )
    db.add(email_model)
    db.commit()
    send_confirmation_mail(user_model)
    return user_model


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()


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

