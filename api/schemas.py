from pydantic import BaseModel, ValidationError, validator
import re


class UserRegister(BaseModel):
    username: str
    email: str
    password1: str
    password2: str

    @validator("email")
    def validate_email(cls, email):
        if not re.match(r"[a-zA-Z0-9.]+@[a-zA-Z]+\.[a-z]+", email):
            raise ValueError("Invalid email address")
        return email

    @validator("password2")
    def validate_passwords(cls, password2, values):
        password1 = values['password1']
        if password1 != password2:
            raise ValueError("Password are not same")
        return password2
