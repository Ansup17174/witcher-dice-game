from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = relationship("Email", back_populates="user", uselist=False, cascade="all, delete")
    password = Column(String(100), nullable=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete")


class UserProfile(Base):
    __tablename__ = "userprofiles"

    user = relationship("User", back_populates="profile")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

    matches_won = Column(Integer, server_default="0", nullable=False)
    matches_lost = Column(Integer, server_default="0", nullable=False)
    matches_played = Column(Integer, server_default="0", nullable=False)


class Email(Base):
    __tablename__ = "emails"

    address = Column(String(100), unique=True, nullable=False)
    activation_token = Column(String(100), nullable=True)
    is_confirmed = Column(Boolean, default=False)
    expiry_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="email")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

