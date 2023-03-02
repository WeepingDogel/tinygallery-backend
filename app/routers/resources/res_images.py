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


@image_resources_api.get("/images/{page}")
async def get_images_as_json(page: int, db: Session = Depends(get_db)):
    if not page:
        raise HTTPException(
            status_code=400, detail="You must append a page number to the end of the url.")

    posts_from_db = crud.get_images_by_page(db=db, page=page)

    list_for_return: list[dict] = []
    for x in posts_from_db:
        temp_dict = {
            "id": str(x.id),
            "post_type": str(x.post_type),
            "description": str(x.description),
            "share_num": int(x.share_num),
            "post_uuid": str(x.post_uuid),
            "nsfw": int(x.nsfw),
            "user_name": str(x.user_name),
            "post_title": str(x.post_title),
            "dots": int(x.dots),
            "date": str(x.date),
            "files": dir_tool.get_files_url_as_dict(str(x.post_uuid))
        }
        list_for_return.append(temp_dict)

    return list_for_return


@image_resources_api.get("/avatar/{user_name_for_get_avatar}")
def get_avatar_by_user_name(user_name_for_get_avatar: str):
    pass


@image_resources_api.get("/profile/background/{user_name_for_get_background}")
def get_background_by_user_name(user_name_for_get_background: str):
    pass
