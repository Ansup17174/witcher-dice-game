from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = relationship("EmailModel", back_populates="user", uselist=False, cascade="all, delete")
    password = Column(String(100), nullable=False)
    stats = relationship("UserStatsModel", back_populates="user", cascade="all, delete")


class UserStatsModel(Base):
    __tablename__ = "userstats"

    user = relationship("UserModel", back_populates="stats")
    user_id = Column(String, ForeignKey("users.id"))

    id = Column(String, primary_key=True)
    game = Column(String(50), nullable=False)
    matches_won = Column(Integer, server_default="0", nullable=False)
    matches_lost = Column(Integer, server_default="0", nullable=False)
    matches_played = Column(Integer, server_default="0", nullable=False)


class EmailModel(Base):
    __tablename__ = "emails"

    address = Column(String(100), unique=True, nullable=False)
    activation_token = Column(String(100), nullable=True)
    is_confirmed = Column(Boolean, default=False)
    expiry_date = Column(DateTime, nullable=True)

    user = relationship("UserModel", back_populates="email")
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)

