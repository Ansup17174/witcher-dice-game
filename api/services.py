from sqlalchemy.orm import Session
from .schemas import UserRegister
from uuid import uuid4
from .models import User, Email


def register_user(db: Session, user_data: UserRegister):
    user_model = User(id=uuid4(), username=user_data.username, password=user_data.second_password)
    db.add(user_model)
    email_model = Email(address=user_data.email, user_id=user_model.id)
    db.add(email_model)
    db.commit()
    db.refresh(user_model)
    return user_model

