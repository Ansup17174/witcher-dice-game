from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = relationship("Email", back_populates="user", uselist=False)
    password = Column(String(100), nullable=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "userprofiles"

    user = relationship("User", back_populates="profile")
    user_id = Column(ForeignKey("users.id"), primary_key=True)

    matches_won = Column(Integer, default=0)
    matches_lost = Column(Integer, default=0)
    matches_played = Column(Integer, default=0)


class Email(Base):
    __tablename__ = "emails"

    address = Column(String(100), unique=True, nullable=False)
    activation_token = Column(String(100), nullable=True)
    is_confirmed = Column(Boolean, default=False)

    user = relationship("User", back_populates="email")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

