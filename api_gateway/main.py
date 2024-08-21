from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import *
from .base_endpoint import BaseEndpoint
from .api_email import email_router

app = FastAPI()
base_endpoint = BaseEndpoint()

app.include_router(auth_router)
app.include_router(reg_router)
app.include_router(users_router)
app.include_router(email_router)

app.include_router(video_router)
app.include_router(base_endpoint.get_router())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "hello!!!"}
