from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from PIL import Image

from ...dependencies.oauth2scheme import oauth2Scheme
from ...model import crud
from app.dependencies.db import get_db
from ... import config
from ...utilities import token_tools as token_tool
import os, uuid

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


# @Post_router.post("/test")
# def testToken(token: str = Depends(oauth2Scheme)) -> str:
#     return TokenTool.GetUserNameByToken(token)

# @Post_router.get("/test")
# def testGetUserByName(db: Session = Depends(get_db)):
#     if crud.GetUserByName(db,user_name="WeepingDogel"):
#         return True
#     else:
#         return  False


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
    # -- end declare block

    # This block for verification
    # ---verification block
    if not crud.get_user_by_name(db, user_name=user_name):
        raise HTTPException(
            status_code=400, detail="The user does not exist!")
    if uploaded_file.__len__() > 1:
        is_multiple = "multiple"

    # Create the post direction witch named its uuid in IMAGE_DIR from config.py.
    current_post_path_obj = Path(os.path.join(config.IMAGE_DIR, post_uuid))
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
    # --- end verification block

    # This block for IO operating
    # --- IO block
    # If the uploaded image files more than one then they will rename as loop count.
    if is_multiple:
        i: int = 0
        for x in uploaded_file:
            suffix: str = x.filename.split(".")[-1]
            current_loop_filename = str(i) + "." + suffix
            i = i + 1
            try:
                with open(str(current_post_path_obj.joinpath(current_loop_filename)), "wb") as f:
                    content = x.file.read()
                    f.write(content)
            except IOError:
                raise HTTPException(
                    status_code=500, detail="Cannot save images on server.")
    else:
        try:
            with open(str(current_post_path_obj.joinpath(uploaded_file[0].filename)), "wb") as f:
                content = uploaded_file[0].file.read()
                f.write(content)
        except IOError:
            raise HTTPException(
                status_code=500, detail="Cannot save images on server.")
    # Save the cover image file in a dir that named "cover", if cover existed.
    if cover:
        try:
            with open(str(current_post_path_obj.joinpath("cover", cover.filename)), "wb") as f:
                content = cover.file.read()
                f.write(content)
        except IOError:
            raise HTTPException(
                status_code=500, detail="Cannot save images on server.")
    # If user does not posts a cover, the cover will auto select from uploaded image files.
    else:
        try:
            with open(str(current_post_path_obj.joinpath("cover", uploaded_file[0].filename)), "wb") as f:
                content = uploaded_file[0].file.read()
                f.write(content)
        except IOError:
            raise HTTPException(
                status_code=500, detail="Cannot save images on server.")
    # --- end IO block

    # This block for compress images.
    # --- compress block
    compressed_cover_path = current_post_path_obj.joinpath("compressedCover")
    compressed_cover_path.mkdir()

    original_cover_path: Path = current_post_path_obj.joinpath("cover", cover.filename)

    try:
        with Image.open(original_cover_path) as f:
            transform_str_path: str = str(original_cover_path)
            cover_file_name: str = original_cover_path.name
            if transform_str_path.split(".")[-1] == "gif" or transform_str_path.split(".")[-1] == "webp":
                f.info["duration"] = 100
            f.thumbnail(size=config.size)
            f.save(compressed_cover_path.joinpath(cover_file_name), optimize=True, quality=config.quality)
    except:
        raise HTTPException(
            status_code=500, detail="Cannot save images on server.")
    # --- end compress block

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


@Post_router.delete("/remove/{post_uuid_for_remove}")
def remove_post_by_uuid(post_uuid_for_remove: str):
    pass


@Post_router.put("/update/{post_uuid_for_update}")
def update_post_by_uuid(post_uuid_for_remove: str):
    pass
