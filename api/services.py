from sqlalchemy.orm import Session
from .schemas import UserRegister
from uuid import uuid4, UUID
from .models import User, Email
from .config import password_context
from .utils import send_confirmation_mail


def register_user(db: Session, user_data: UserRegister):
    hashed_password = password_context.hash(user_data.password)
    user_model = User(id=uuid4(), username=user_data.username, password=hashed_password)
    db.add(user_model)
    email_token = str(uuid4())
    email_model = Email(address=user_data.email, user_id=user_model.id, activation_token=email_token)
    db.add(email_model)
    db.commit()
    send_confirmation_mail(user_model)
    return user_model


def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.id == user_id).first()
