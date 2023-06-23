from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import uuid

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
def upload_image(is_nsfw: str = Form(),
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
    post_uuid: str = str(uuid.uuid4())
    # If User uploaded a cover then this variable will be True.
    cover_exist: bool = False
    # -- end declare block

    # This block for verification
    # ---verification block
    if not crud.get_user_by_name(db, user_name=user_name) and not crud.get_admin_by_name(db, user_name=user_name):
        raise HTTPException(
            status_code=400, detail="The user does not exist!")
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

    save_post_status: bool = dir_tool.save_post_images(
        post_uuid=post_uuid,
        uploaded_file=uploaded_file,
        supplementary_mode=False
    )
    if not save_post_status:
        raise HTTPException(
            status_code=400, detail="Cannot save the post on server!")

    save_cover_status: bool = dir_tool.save_post_cover(
        cover_name=uploaded_file[0].filename,
        post_uuid=post_uuid,
        cover=cover,
        cover_exist=cover_exist,
        update_mode=False
    )
    if not save_cover_status:
        raise HTTPException(
            status_code=400, detail="Cannot save the cover of post on server!")

    compress_cover_status: bool = dir_tool.compress_cover(
        post_uuid=post_uuid,
        update_mode=False
    )
    if not compress_cover_status:
        raise HTTPException(
            status_code=400, detail="Cannot compress the cover of post on server!")

    if is_nsfw == "true":
        nsfw_db: bool = True
    else:
        nsfw_db: bool = False

    crud.db_create_post(
        db=db,
        user_name=user_name,
        post_title=post_title,
        description=description,
        post_uuid=post_uuid,
        is_nsfw=nsfw_db
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
                        cover: UploadFile,
                        supplementary_mode: bool = Form(),
                        uploaded_file: list[UploadFile] = File(),
                        is_nsfw: str = Form(),
                        post_title: str = Form(),
                        description: str = Form(),
                        db: Session = Depends(get_db),
                        token: str = Depends(oauth2Scheme)):
    # This block for declare variables.
    # --- declare block
    # Get the name of user from token
    user_name: str = token_tool.get_user_name_by_token(token=token)
    # If User uploaded a cover then this variable will be True.
    cover_exist: bool = False
    # This variable will change only cover_exist.
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
    if cover:
        cover_exist = True
        cover_filename = cover.filename
    # Return Error, if you have same file name in uploaded files .
    for x in uploaded_file:
        if x.filename in uploaded_file:
            raise HTTPException(
                status_code=400, detail="File name not be same!")

    current_post_path_obj = Path(config.POST_DIR).joinpath(post_uuid_for_update)
    # If the direction does not exist then return error.
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
    save_post_status: bool = dir_tool.save_post_images(
        supplementary_mode=supplementary_mode,
        post_uuid=post_uuid_for_update,
        uploaded_file=uploaded_file
    )
    if not save_post_status:
        raise HTTPException(
            status_code=400, detail="Cannot save the post on server!")

    save_cover_status: bool = dir_tool.save_post_cover(
        cover_name=cover_filename,
        post_uuid=post_uuid_for_update,
        cover_exist=cover_exist,
        cover=cover,
        update_mode=True
    )
    if not save_cover_status:
        raise HTTPException(
            status_code=400, detail="Cannot save the cover of post on server!")

    compress_cover_status: bool = dir_tool.compress_cover(
        post_uuid=post_uuid_for_update,
        update_mode=True
    )
    if not compress_cover_status:
        raise HTTPException(
            status_code=400, detail="Cannot compress the cover of post on server!")
    # -- End IO block

    if is_nsfw == "true":
        nsfw_db: bool = True
    else:
        nsfw_db: bool = False

    # Update database.
    crud.update_post_by_uuid(
        db=db,
        post_uuid=post_uuid_for_update,
        is_nsfw=nsfw_db,
        post_title=post_title,
        post_description=description
    )
    return {"status": "success"}
