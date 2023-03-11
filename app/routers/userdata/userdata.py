import random
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from pathlib import Path
from ...dependencies.oauth2scheme import oauth2Scheme
from ...dependencies.db import get_db
from ... import config
from ...utilities.userdata_tool import auth_user_by_name
from ...utilities.token_tools import get_user_name_by_token
from ...utilities.dir_tool import save_user_avatar

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


@userdata_router.put("/get/username")
def get_user_name(token: str = Depends(oauth2Scheme)):
    user_name = get_user_name_by_token(token=token)
    return {'username': user_name}


@userdata_router.put("/set/background")
def create_user_profile_background(background: UploadFile,
                                   token: str = Depends(oauth2Scheme),
                                   db: Session = Depends(get_db)):
    file_suffix: str = background.filename.split(".")[-1]
    user_uuid = auth_user_by_name(db=db, token=token)
    background_path: Path = Path(config.BACKGROUND_DIR + "/" + user_uuid)
    if background_path.exists():
        shutil.rmtree(background_path)
    background_path.mkdir(exist_ok=True)
    try:
        with open(str(background_path.joinpath(user_uuid + str(random.randint(0, 9999)) + "." + file_suffix)), "wb") as f:
            content = background.file.read()
            f.write(content)
    except IOError:
        print(IOError)
        # raise HTTPException(
        #     status_code=500, detail="Cannot save file on server.")

    return {"status": "success"}


@userdata_router.delete("/delete/background")
def delete_user_profile_background(token: str = Depends(oauth2Scheme),
                                   db: Session = Depends(get_db)):
    pass


@userdata_router.put("/set/avatar")
def create_user_avatar(avatar: UploadFile,
                       db: Session = Depends(get_db),
                       token: str = Depends(oauth2Scheme)):
    avatar_path: Path = Path(config.AVATAR_DIR)
    user_uuid = auth_user_by_name(db=db, token=token)
    file_suffix = avatar.filename.split(".")[-1]
    if not save_user_avatar(avatar=avatar, user_uuid=user_uuid, file_suffix=file_suffix, avatar_path=avatar_path):
        raise HTTPException(
            status_code=500,
            detail="Cannot save file one server."
        )
    else:
        return {"status": "success"}
    # try:
    #     with open(str(avatar_path.joinpath(user_uuid + "." + file_suffix)), "wb") as f:
    #         content = avatar.file.read()
    #         f.write(content)
    #
    # except IOError:
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Cannot save file on server."
    #     )


@userdata_router.delete("/delete/avatar/{user_name}")
def delete_user_avatar(user_name: str):
    pass
