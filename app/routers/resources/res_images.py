from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from app.dependencies.db import get_db
from ...model import crud
from ...utilities import dir_tool
from ...utilities.userdata_tool import get_user_uuid_by_name
from ... import config

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
            "id": x.id,
            "description": x.description,
            "share_num": x.share_num,
            "post_uuid": x.post_uuid,
            "nsfw": x.nsfw,
            "user_name": x.user_name,
            "post_title": x.post_title,
            "dots": x.dots,
            "date": x.date[0:16],
            "cover_url": dir_tool.get_cover_file_url(x.post_uuid),
            "avatar": dir_tool.get_avatar_file_url(dir_user_uuid=get_user_uuid_by_name(user_name=x.user_name, db=db))[1]
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
        "date": post_db.date[0:16],
        "files_url": dir_tool.get_files_url_as_dict(post_db.post_uuid)
    }

    return temp_dict


@image_resources_api.get("/posts/getAllPostsBelongToUser/{page}")
def get_all_posts_belong_to_user(page: int, user_name: str, db: Session = Depends(get_db)):
    return crud.get_all_posts_belong_to_user(db=db, user_name=user_name, page=page)


@image_resources_api.get("/avatar/{user_name_for_get_avatar}")
def get_avatar_by_user_name(user_name_for_get_avatar: str, db: Session = Depends(get_db)):
    user_uuid = get_user_uuid_by_name(user_name=user_name_for_get_avatar, db=db)
    resource_server = config.AVATARS_RESOURCE_SERVER_URL.split('/static/')[0]
    avatar_dir = Path(config.AVATAR_DIR)
    avatar_200px_dir = Path(avatar_dir.joinpath(user_uuid + '/200'))
    avatar_40px_dir = Path(avatar_dir.joinpath(user_uuid + '/40'))
    avatar_200px = resource_server + "/" + str(list(avatar_200px_dir.glob('*.*'))[0])
    avatar_40px = resource_server + "/" + str(list(avatar_40px_dir.glob('*.*'))[0])
    return {
        'status': "success",
        'avatar_200px': avatar_200px,
        'avatar_40px': avatar_40px
    }


@image_resources_api.get("/profile/background/{user_name_for_get_background}")
def get_background_by_user_name(user_name_for_get_background: str, db: Session = Depends(get_db)):
    user_uuid = get_user_uuid_by_name(user_name=user_name_for_get_background, db=db)
    resource_server = config.POSTS_RESOURCE_SERVER_URL.split('/static/')[0]
    background_dir = Path(config.BACKGROUND_DIR)
    background_image_dir = Path(background_dir.joinpath(user_uuid))
    background_image = resource_server + "/" + str(list(background_image_dir.glob("*.*"))[0])
    return {
        'status': 'success',
        'background': background_image
    }
