from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path

from ...dependencies.oauth2scheme import oauth2Scheme
from ...model import crud
from ...db import get_db
from ... import config
from ...utilities import token_tools as token_tool
import os, uuid, time

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

@UploadRouter.post("/uploadtest")
def upload_test(files: list[UploadFile] = File()):
    if files[0].filename.split(".")[-1] in config.ALLOW_SUFFIX:
        return {"status": "yes"}
    return {"suffix": files[0].filename.split(".")[-1]}


@UploadRouter.post("/image")
async def upload_image(is_nsfw: bool = Form(),
                       db: Session = Depends(get_db),
                       uploaded_file: list[UploadFile] = File(),
                       cover: UploadFile | None = None,
                       post_title: str = Form(),
                       description: str = Form(),
                       token: str = Depends(oauth2Scheme)):
    # Get the name of user from token
    user_name: str = token_tool.get_user_name_by_token(token=token)
    # If the images that user uploaded is multiple then this variable will be True.
    is_multiple: bool = False
    # If a user uploaded a cover then this variable will be True
    have_cover: bool = False
    post_uuid: str = str(uuid.uuid4())
    date: str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if not crud.get_user_by_name(db, user_name=user_name):
        raise HTTPException(
            status_code=400, detail="The user does not exist!")
    if uploaded_file.__len__() > 1:
        is_multiple = True
    if cover:
        have_cover = True

    # Create the post direction witch named its uuid in IMAGE_DIR from config.py.
    current_post_path_obj = Path(os.path.join(config.IMAGE_DIR, post_uuid))
    # If the direction already existed return error.
    if current_post_path_obj.is_dir():
        raise HTTPException(
            status_code=500, detail="Cannot to create post.")
    current_post_path_obj.mkdir()
    current_post_path_obj.joinpath("cover").mkdir()

    # Check image files suffix.
    for x in uploaded_file:
        if x.filename.split(".")[-1] not in config.ALLOW_SUFFIX:
            raise HTTPException(
                status_code=400, detail="Not allowed file type.")
    if cover:
        if cover.filename.split(".")[-1] not in config.ALLOW_SUFFIX:
            raise HTTPException(
                status_code=500, detail="Not allowed file type.")

    # If the uploaded image files more than one then they will rename as loop count.
    if is_multiple:
        i: int = 0
        for x in uploaded_file:
            suffix: str = x.filename.split(".")[-1]
            current_loop_filename = str(i) + "." + suffix
            i = i + 1
            with open(str(current_post_path_obj.joinpath(current_loop_filename)), "wb") as f:
                content = x.file.read()
                f.write(content)
    else:
        with open(str(current_post_path_obj.joinpath(uploaded_file[0].filename)), "wb") as f:
            content = uploaded_file[0].file.read()
            f.write(content)
    # Save the cover image file that named "cover", if cover existed.
    if cover:
        with open(str(current_post_path_obj.joinpath("cover", cover.filename)), "wb") as f:
            content = cover.file.read()
            f.write(content)
    # If user does not upload a cover, the cover will auto select from uploaded image files.
    else:
        with open(str(current_post_path_obj.joinpath("cover", uploaded_file[0].filename)), "wb") as f:
            content = uploaded_file[0].file.read()
            f.write(content)

    if is_multiple:
        post_type_db = "multiple"
    else:
        post_type_db = "single"

    crud.db_create_post(
        db=db,
        user_name=user_name,
        post_type=post_type_db,
        post_title=post_title,
        description=description,
        post_uuid=post_uuid,
        is_nsfw=is_nsfw
    )

    return {
        "status": "success"
    }
