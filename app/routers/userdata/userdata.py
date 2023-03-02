from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from pathlib import Path

from ...dependencies.oauth2scheme import oauth2Scheme
from ...dependencies.db import get_db
from ...utilities import token_tools as token_tool
from ... import config
from ...model import crud

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


def auth_user_by_name(db: Session, token: str) -> str:
    user_name_from_token: str = token_tool.get_user_name_by_token(token=token)
    if not user_name_from_token:
        raise HTTPException(
            status_code=400, detail="The user does not exist!")

    user_name_from_db = crud.get_user_by_name(db, user_name=user_name_from_token)
    if not user_name_from_db:
        raise HTTPException(
            status_code=400, detail="The user does not exist!")

    return user_name_from_db.users_uuid


@userdata_router.post("/set/background")
def create_user_profile_background(background: UploadFile,
                                   token: str = Depends(oauth2Scheme),
                                   db: Session = Depends(get_db)):
    background_path: Path = Path(config.BACKGROUND_DIR)
    file_suffix: str = background.filename.split(".")[-1]

    user_uuid = auth_user_by_name(db=db, token=token)

    try:
        with open(str(background_path.joinpath(user_uuid + "." + file_suffix)), "wb") as f:
            content = background.file.read()
            f.write(content)
    except IOError:
        raise HTTPException(
            status_code=500, detail="Cannot save file on server.")

    return {"status": "success"}


@userdata_router.delete("/delete/background")
def delete_user_profile_background(token: str = Depends(oauth2Scheme),
                                   db: Session = Depends(get_db)):
    pass


@userdata_router.post("/set/avatar/{user_name}")
def create_user_avatar(user_name: str):
    pass


@userdata_router.delete("/delete/avatar/{user_name}")
def delete_user_avatar(user_name: str):
    pass
