from fastapi import FastAPI
from .schemas import UserRegister

app = FastAPI()


@app.get("/auth/register")
async def register(data: UserRegister):
    return data
