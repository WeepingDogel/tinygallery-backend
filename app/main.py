# Import necessary dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers.auth import user
from .routers.posts import image
from .routers.resources import res_images
from .routers.remark import remarks
from .routers.userdata import userdata
from .routers.Likes import likes
from .routers.admin import admin
from .model import models
from .utilities.dir_tool import create_all_project_dir
from app.dependencies.db import engine
from app.utilities.admin_tool import create_admin_users

# Define tags metadata for API documentation
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

# Define project description
document_description = """
This project is under **development**, only 
* /user/register,
* /user/token,
* /posts/create,
* /post/delete,
* /posts/update,
* /resources/posts/,
* /resources/posts/single,
* /userdata/get/username,
* /userdata/change-password,
* /resources/avatar/{user_name_for_get_avatar},
* /resources/profile/background/{user_name_for_get_background}

interfaces are available.
"""

# Create FastAPI app instance with tags and description
app = FastAPI(openapi_tags=tags_metadata, description=document_description)

# Set allowed origins for CORS middleware
origins = [
    "*",
]

# Add CORS middleware to app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create necessary project directories
create_all_project_dir()

# Include routers for various endpoints
app.include_router(user.userAuthRouter)
app.include_router(image.Post_router)
app.include_router(res_images.image_resources_api)
app.include_router(remarks.Remark_router)
app.include_router(userdata.userdata_router)
app.include_router(likes.likes_api)
app.include_router(admin.admin_auth_router)

# Mount the directory of static files.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database models
models.Base.metadata.create_all(bind=engine)
create_admin_users()


# Define root route for API
@app.get("/")
def read_root():
    return {'Data': 'Hello World! This is the backend of TinyGallery created by WeepingDogel!'}
