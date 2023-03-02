from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.auth import user
from .routers.posts import image
from .routers.resources import res_images
from .routers.remark import remarks
from .model import models
from .utilities.dir_tool import create_all_project_dir
from app.dependencies.db import engine

tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users, the **login** logic is also here."
    },
    {
        "name": "Posts",
        "description": "Operations with posts."
    },
    {
        "name": "Resources",
        "description": "The exit of all static files."
    },
    {
        "name": "Remarks",
        "description": "Operations with remarks"
    }
]

document_description = """
This project is under **development**, only 
* /user/register,
* /user/token,
* /posts/create,
* /resources/posts/,

interface are available.
"""

app = FastAPI(openapi_tags=tags_metadata, description=document_description)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

create_all_project_dir()

app.include_router(user.userAuthRouter)
app.include_router(image.Post_router)
app.include_router(res_images.image_resources_api)
app.include_router(remarks.Remark_router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {'Data': 'Hello World! This is the backend of TinyGallery created by WeepingDogel!'}
