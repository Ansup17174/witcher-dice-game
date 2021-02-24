from pydantic import BaseModel, validator
from uuid import UUID
import re
import string


class EmailSchema(BaseModel):
    address: str
    is_confirmed: bool

    class Config:
        orm_mode = True


class UserProfileSchema(BaseModel):
    matches_won: int
    matches_lost: int
    matches_played: int

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: UUID
    username: str
    email: EmailSchema
    profile: UserProfileSchema

    class Config:
        orm_mode = True


class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password1: str
    password2: str

    @validator("email")
    def validate_email(cls, email):
        if not re.match(r"[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-z]+", email):
            raise ValueError("Invalid email address")
        return email

    @validator("password1")
    def validate_password(cls, password1):
        if len(password1) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(password1) > 32:
            raise ValueError("Password must be at most 32 characters long")
        return password1

    @validator("password2")
    def validate_passwords(cls, password2, values):
        password1 = values['password1']
        if password1 != password2:
            raise ValueError("Password are not same")
        return password2


class ResendEmailSchema(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, email):
        if not re.match(r"[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-z]+", email):
            raise ValueError("Invalid email address")
        return email


class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
