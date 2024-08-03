from fastapi import FastAPI
from .routers import *
from .base_endpoint import BaseEndpoint

app = FastAPI()
base_endpoint = BaseEndpoint()

app.include_router(auth_router)
app.include_router(reg_router)
app.include_router(users_router)

app.include_router(video_router)
app.include_router(base_endpoint.get_router())


@app.get("/")
def index():
    return {"message": "hello!!!"}
