from pydantic import BaseModel, validator
from typing import Optional
from uuid import UUID
import re


class Email(BaseModel):
    address: str
    is_confirmed: bool

    class Config:
        orm_mode = True


class UserProfile(BaseModel):
    matches_won: int
    matches_lost: int
    matches_played: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: UUID
    username: str
    email: Email
    profile: UserProfile

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    second_password: str

    @validator("email")
    def validate_email(cls, email):
        if not re.match(r"[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-z]+", email):
            raise ValueError("Invalid email address")
        return email

    @validator("second_password")
    def validate_passwords(cls, second_password, values):
        password = values['password']
        if password != second_password:
            raise ValueError("Password are not same")
        return second_password


class ResendEmail(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, email):
        if not re.match(r"[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-z]+", email):
            raise ValueError("Invalid email address")
        return email


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
