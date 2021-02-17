from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password1: str
    password2: str
