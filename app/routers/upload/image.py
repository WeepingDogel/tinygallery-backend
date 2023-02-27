from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session

from ...dependencies.oauth2scheme import oauth2Scheme
from ...model import crud
from ...db import get_db
from ... import config
from ...utilities import token_tools as token_tool
import os

UploadRouter = APIRouter(
    prefix="/upload",
    tags=['Upload'],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


# @UploadRouter.post("/test")
# def testToken(token: str = Depends(oauth2Scheme)) -> str:
#     return TokenTool.GetUserNameByToken(token)

# @UploadRouter.get("/test")
# def testGetUserByName(db: Session = Depends(get_db)):
#     if crud.GetUserByName(db,user_name="WeepingDogel"):
#         return True
#     else:
#         return  False

@UploadRouter.post("/image")
async def upload_image(is_nsfw: bool = Form(),
                       db: Session = Depends(get_db),
                       cover: UploadFile | None = None,
                       file: list[UploadFile] = File(),
                       post_title: str = Form(),
                       description: str = Form(),
                       token: str = Depends(oauth2Scheme)):
    user_name = token_tool.get_user_name_by_token(token=token)
    if crud.get_user_by_name(db, user_name=user_name):
        if not os.path.exists(config.IMAGE_DIR):
            os.mkdir(config.IMAGE_DIR)
        crud.db_create_post(
            user_name=user_name,
            post_title=post_title,
            description=description,
            is_nsfw=is_nsfw
        )
        return {"status": "Success"}
    else:
        raise token_tool.CredentialsException
