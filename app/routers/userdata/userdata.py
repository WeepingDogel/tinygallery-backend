import random
import shutil
from tzlocal import get_localzone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile  # Importing necessary modules
from sqlalchemy.orm import Session

from ...model.crud import get_posts_quantity, get_user_quantity, get_comments_quantity
from ... import config
from ...dependencies.db import get_db
from ...dependencies.oauth2scheme import oauth2Scheme
from ...utilities.dir_tool import save_user_avatar
from ...utilities.token_tools import get_user_name_by_token
from ...utilities.userdata_tool import auth_user_by_name

# Creating a new APIRouter object with a prefix, tags, dependencies and responses defined.
userdata_router = APIRouter(
    prefix="/userdata",
    tags=['User data'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


# Endpoint for getting user name using token
@userdata_router.get("/get/username")
def get_user_name(token: str = Depends(oauth2Scheme)):
    user_name = get_user_name_by_token(token=token)
    return {'username': user_name}


# Endpoint for setting user profile background image
@userdata_router.put("/set/background")
def create_user_profile_background(background: UploadFile,
                                   token: str = Depends(oauth2Scheme),
                                   db: Session = Depends(get_db)):
    file_suffix: str = background.filename.split(".")[-1]  # Extracting file extension from filename
    user_uuid = auth_user_by_name(db=db, token=token)  # Authenticating user using token
    background_path: Path = Path(config.BACKGROUND_DIR + "/" + user_uuid)  # Defining the path to store background image
    if background_path.exists():  # Removing existing background image
        shutil.rmtree(background_path)
    background_path.mkdir(exist_ok=True)  # Creating directory to store the background image
    try:
        with open(str(background_path.joinpath(user_uuid + str(random.randint(0, 9999)) + "." + file_suffix)), "wb") \
                as f:  # Saving the background image with a random number added to its filename.
            content = background.file.read()
            f.write(content)
    except IOError:
        print(IOError)

    return {"status": "success"}


# Endpoint for deleting user profile background image
@userdata_router.delete("/delete/background")
def delete_user_profile_background(token: str = Depends(oauth2Scheme),
                                   db: Session = Depends(get_db)):
    pass


# Endpoint for setting user avatar image
@userdata_router.put("/set/avatar")
def create_user_avatar(avatar: UploadFile,
                       db: Session = Depends(get_db),
                       token: str = Depends(oauth2Scheme)):
    avatar_path: Path = Path(config.AVATAR_DIR)  # Defining the path to store avatar image
    user_uuid = auth_user_by_name(db=db, token=token)  # Authenticating user using token
    file_suffix = avatar.filename.split(".")[-1]  # Extracting file extension from filename
    if not save_user_avatar(avatar=avatar, user_uuid=user_uuid, file_suffix=file_suffix, avatar_path=avatar_path):
        # If the avatar image cannot be saved on the server, return an HTTPException with status code and details.
        raise HTTPException(
            status_code=500,
            detail="Cannot save file one server."
        )
    else:
        return {"status": "success"}  # On success, return status message


# Endpoint for deleting user avatar image
@userdata_router.delete("/delete/avatar/{user_name}")
def delete_user_avatar(user_name: str):
    pass  # Placeholder code – function yet to be implemented


@userdata_router.get('/get/user_num')
def get_users_num(db: Session = Depends(get_db)):
    users_num = get_user_quantity(db=db)
    return users_num


@userdata_router.get('/get/posts_num')
def get_posts_num(db: Session = Depends(get_db)):
    posts_num = get_posts_quantity(db=db)
    return posts_num


@userdata_router.get('/get/comments_num')
def get_comments_num(db: Session = Depends(get_db)):
    comments_num = get_comments_quantity(db=db)
    return comments_num


@userdata_router.get("/get/timezone")
def get_server_timezone():
    tz = str(get_localzone())
    return tz
