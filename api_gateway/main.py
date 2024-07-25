from fastapi import FastAPI
from .routers import *

app = FastAPI()

app.include_router(auth_router)
app.include_router(reg_router)
app.include_router(users_router)
app.include_router(video_router)


@app.get("/")
def index():
    return {"message": "hello!!!"}
