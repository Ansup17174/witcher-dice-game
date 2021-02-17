from fastapi import FastAPI
from .schemas import UserRegister

app = FastAPI()


@app.post("/auth/register")
async def register(data: UserRegister):
    return data
