import shutil

from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import os, uuid

from ...dependencies.oauth2scheme import oauth2Scheme
from ...model import crud
from app.dependencies.db import get_db
from ... import config
from ...utilities import token_tools as token_tool
from ...utilities import dir_tool

Post_router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


@Post_router.post("/create")
async def upload_image(is_nsfw: bool = Form(),
                       db: Session = Depends(get_db),
                       uploaded_file: list[UploadFile] = File(),
                       cover: UploadFile | None = None,
                       post_title: str = Form(),
                       description: str = Form(),
                       token: str = Depends(oauth2Scheme)):
    # This block for declare variables.
    # --- declare block
    # Get the name of user from token
    user_name: str = token_tool.get_user_name_by_token(token=token)
    # If the images that user uploaded is multiple then this variable will be "multiple".
    is_multiple: str = "single"
    post_uuid: str = str(uuid.uuid4())
    # If User uploaded a cover then this variable will be True.
    cover_exist: bool = False
    # -- end declare block

    # This block for verification
    # ---verification block
    if not crud.get_user_by_name(db, user_name=user_name):
        raise HTTPException(
            status_code=400, detail="The user does not exist!")
    if uploaded_file.__len__() > 1:
        is_multiple = "multiple"
    if cover:
        cover_exist = True
    # Return Error, if list have same file name.
    for x in uploaded_file:
        if x.filename in uploaded_file:
            raise HTTPException(
                status_code=400, detail="File name not be same!")

    # Create the post direction witch named its uuid in IMAGE_DIR from config.py.
    current_post_path_obj = Path(config.POST_DIR).joinpath(post_uuid)
    # If the direction already existed then return error.
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

    try:
        dir_tool.save_post_images(
            is_multiple=is_multiple,
            post_uuid=post_uuid,
            uploaded_file=uploaded_file,
            supplementary_mode=False
        )
    except IOError:
        raise HTTPException(
            status_code=500, detail="Cannot save image on server.")

    try:
        dir_tool.save_post_cover(
            auto_cover_name=uploaded_file[0].filename,
            post_uuid=post_uuid,
            cover=cover,
            cover_exist=cover_exist,
            supplementary_mode=False
        )
    except IOError:
        raise HTTPException(
            status_code=500, detail="Cannot save cover on server.")

    try:
        dir_tool.compress_cover(
            post_uuid=post_uuid,
            cover_exist=cover_exist,
            cover_name=cover,
            auto_cover_name=uploaded_file[0].filename
        )
    except IOError:
        raise HTTPException(
            status_code=500, detail="Cannot compress cover.")

    crud.db_create_post(
        db=db,
        user_name=user_name,
        post_type=is_multiple,
        post_title=post_title,
        description=description,
        post_uuid=post_uuid,
        is_nsfw=is_nsfw
    )

    return {
        "status": "success"
    }


def auth_post_owner(token_for_auth: str, post_uuid: str, db: Session) -> bool:
    user_name_from_token = token_tool.get_user_name_by_token(token=token_for_auth)

    the_post_obj = crud.get_single_post_by_uuid(db=db, post_uuid=post_uuid)

    if user_name_from_token != the_post_obj.user_name:
        return False

    return True


@Post_router.delete("/remove/{post_uuid_for_remove}")
def remove_post_by_uuid(post_uuid_for_remove: str,
                        db: Session = Depends(get_db),
                        token: str = Depends(oauth2Scheme)):
    if not auth_post_owner(db=db, token_for_auth=token, post_uuid=post_uuid_for_remove):
        raise HTTPException(
            status_code=500, detail="You cannot delete a post that is  not yours.")
    # Update database
    if crud.remove_post_by_uuid(db=db, post_uuid=post_uuid_for_remove) == 0:
        raise HTTPException(
            status_code=500, detail="Cannot remove post.")
    if not dir_tool.remove_post_folder_by_uuid(post_uuid_for_remove):
        raise HTTPException(
            status_code=500, detail="Cannot remove post folder.")

    return {"status": "success"}


@Post_router.put("/update/{post_uuid_for_update}")
def update_post_by_uuid(post_uuid_for_update: str,
                        supplementary_mode: bool = Form(),
                        uploaded_file: list[UploadFile] = File(),
                        cover: UploadFile | None = None,
                        is_nsfw: bool = Form(),
                        post_title: str = Form(),
                        description: str = Form(),
                        db: Session = Depends(get_db),
                        token: str = Depends(oauth2Scheme)):
    # This block for declare variables.
    # --- declare block
    # Get the name of user from token
    user_name: str = token_tool.get_user_name_by_token(token=token)
    # If the images that user uploaded is multiple then this variable will be "multiple".
    is_multiple: str = "single"
    # If User uploaded a cover then this variable will be True.
    cover_exist: bool = False
    # This variable only changed when cover_exist.
    cover_filename: str = ""
    # -- end declare block

    # This block for verification
    # ---verification block
    if not crud.get_user_by_name(db, user_name=user_name):
        raise HTTPException(
            status_code=400, detail="The user does not exist!")
    if not auth_post_owner(db=db, token_for_auth=token, post_uuid=post_uuid_for_update):
        raise HTTPException(
            status_code=400, detail="You cannot update a post that is not yours.")
    if uploaded_file.__len__() > 1:
        is_multiple = "multiple"
    if supplementary_mode:
        is_multiple = "multiple"
    if cover:
        cover_exist = True
    # Return Error, if list have same file name.
    for x in uploaded_file:
        if x.filename in uploaded_file:
            raise HTTPException(
                status_code=400, detail="File name not be same!")

    # Create the post direction witch named its uuid in IMAGE_DIR from config.py.
    current_post_path_obj = Path(config.POST_DIR).joinpath(post_uuid_for_update)
    # If the direction already existed then return error.
    if not current_post_path_obj.is_dir():
        raise HTTPException(
            status_code=500, detail="The post does not exist.")

    # Check image files suffix.
    for x in uploaded_file:
        if x.filename.split(".")[-1] not in config.ALLOW_SUFFIX:
            raise HTTPException(
                status_code=400, detail="Not allowed file type.")
    if cover:
        if cover.filename.split(".")[-1] not in config.ALLOW_SUFFIX:
            raise HTTPException(
                status_code=500, detail="Not allowed file type.")
    # --- end verification block

    # ---IO block
    dir_tool.save_post_images(
        is_multiple=is_multiple,
        supplementary_mode=supplementary_mode,
        post_uuid=post_uuid_for_update,
        uploaded_file=uploaded_file
    )

    if cover_exist:
        dir_tool.save_post_cover(
            auto_cover_name=uploaded_file[0].filename,
            post_uuid=post_uuid_for_update,
            cover_exist=cover_exist,
            cover=cover,
            supplementary_mode=supplementary_mode
        )

        dir_tool.compress_cover(
            post_uuid=post_uuid_for_update,
            cover_exist=cover_exist,
            cover_name=cover,
            auto_cover_name=uploaded_file[0].filename
        )
    # -- End IO block

    # Update database.
    if not crud.update_post_by_uuid(db=db, post_uuid=post_uuid_for_update, post_type_update=is_multiple):
        raise HTTPException(
            status_code=500, detail="Cannot update post.")
    return {"status": "success"}
