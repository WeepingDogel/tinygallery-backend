from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from ...model import crud
from ...utilities import dir_tool

image_resources_api = APIRouter(
    prefix="/resources",
    tags=['Resources'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


@image_resources_api.get("/posts/{page}")
async def get_posts_as_json(page: int, db: Session = Depends(get_db)):
    if not page:
        raise HTTPException(
            status_code=400, detail="You must append a page number to the end of the url.")

    posts_from_db = crud.get_posts_by_page(db=db, page=page)

    list_for_return: list[dict] = []
    for x in posts_from_db:
        temp_dict = {
            "id": str(x.id),
            "description": str(x.description),
            "share_num": int(x.share_num),
            "post_uuid": str(x.post_uuid),
            "nsfw": x.nsfw,
            "user_name": str(x.user_name),
            "post_title": str(x.post_title),
            "dots": int(x.dots),
            "date": str(x.date),
            "cover_url": dir_tool.get_cover_file_url(x.post_uuid)
        }
        list_for_return.append(temp_dict)

    return list_for_return


@image_resources_api.get("/posts/single/{post_uuid}")
def get_single_post_images_by_uuid(post_uuid: str, db: Session = Depends(get_db)):
    post_db = crud.get_single_post_by_uuid(db=db, post_uuid=post_uuid)

    if not post_db:
        raise HTTPException(
            status_code=500, detail="The corresponding post does not exist.")

    temp_dict = {
        "id": post_db.id,
        "description": post_db.description,
        "share_num": post_db.share_num,
        "post_uuid": post_db.post_uuid,
        "nsfw": post_db.nsfw,
        "user_name": post_db.user_name,
        "post_title": post_db.post_title,
        "dots": post_db.dots,
        "date": post_db.date,
        "files_url": dir_tool.get_files_url_as_dict(post_db.post_uuid)
    }

    return temp_dict


@image_resources_api.get("/avatar/{user_name_for_get_avatar}")
def get_avatar_by_user_name(user_name_for_get_avatar: str):
    pass


@image_resources_api.get("/profile/background/{user_name_for_get_background}")
def get_background_by_user_name(user_name_for_get_background: str):
    pass
