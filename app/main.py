from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.auth import user
from .model import models
from .db import engine

app = FastAPI()

origins = [
    "http://loaclhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    user.userAuthRouter,
)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {'Data': 'Hello World! This is the backend of TinyGallery created by WeepingDogel!'}

