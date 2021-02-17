from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, default=uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = relationship("Email", back_populates="user", uselist=False)
    password = Column(String(100), nullable=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "userprofiles"

    user = relationship("User", back_populates="profile")
    user_id = Column(ForeignKey("user.id"))

    matches_won = Column(Integer, default=0)


class Email(Base):
    __tablename__ = "emails"

    address = Column(String(100), unique=True, nullable=False)
    activation_token = Column(String(100), nullable=True)
    is_confirmed = Column(Boolean, default=False)

    user = relationship("User", back_populates="email")
    user_id = Column(ForeignKey("user.id"))

