from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.auth import user
from .routers.posts import image
from .routers.resources import res_images
from .model import models
from .db import engine
from .config import IMAGE_DIR
import os

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

app.include_router(user.userAuthRouter)
app.include_router(image.UploadRouter)
app.include_router(res_images.image_resources_api)

models.Base.metadata.create_all(bind=engine)

if not os.path.exists("static"):
    os.mkdir("static")

if not os.path.exists(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)


@app.get("/")
def read_root():
    return {'Data': 'Hello World! This is the backend of TinyGallery created by WeepingDogel!'}
