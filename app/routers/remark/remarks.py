from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Union
from ...model import schemas
from ...dependencies.db import get_db
from ...dependencies.oauth2scheme import oauth2Scheme
from ...model import crud
from ...utilities import token_tools
from ...utilities import dir_tool

Remark_router = APIRouter(
    prefix="/remark",
    tags=['Remarks'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


@Remark_router.post("/create/inpost")
def create_remark_for_post(remark_create: schemas.RemarkCreate,
                           db: Session = Depends(get_db),
                           token: str = Depends(oauth2Scheme)):
    user_name = token_tools.get_user_name_by_token(token=token)
    if not crud.get_user_by_name(user_name=user_name, db=db):
        raise HTTPException(
            status_code=400,
            detail='User does not exist!'
        )
    crud.create_remark(db=db, remark_create=remark_create, user_name=user_name)

    return {
        "status": "success"
    }


@Remark_router.post("/create/reply")
def create_reply_for_remark(reply_create: schemas.ReplyCreate,
                            db: Session = Depends(get_db),
                            token: str = Depends(oauth2Scheme)):
    user_name = token_tools.get_user_name_by_token(token=token)
    if not crud.get_user_by_name(user_name=user_name, db=db):
        raise HTTPException(
            status_code=400,
            detail='User does not exist!'
        )
    crud.create_reply(db=db, reply_create=reply_create, user_name=user_name)
    return {
        "status": "success"
    }


@Remark_router.get("/get/inpost/{post_uuid_for_get_remark}/{page}")
async def get_remark_in_post_by_post_uuid(page: int,
                                          post_uuid_for_get_remark: str,
                                          db: Session = Depends(get_db)):
    remark_from_db = crud.get_remarks_by_post_uuid(post_uuid=post_uuid_for_get_remark,
                                                   page=page, db=db)
    list_for_return: list[dict] = []
    for x in remark_from_db:
        temp_dict = {
            "id": x.id,
            "post_uuid": x.post_uuid,
            "user_uuid": x.user_uuid,
            "user_name": x.user_name,
            "remark_uuid": x.remark_uuid,
            "content": x.content,
            "date": x.date,
            "avatar": dir_tool.get_avatar_file_url(dir_user_uuid=x.user_uuid)[0]
        }
        list_for_return.append(temp_dict)

    return list_for_return


@Remark_router.get('/get/in_remark/single/{remark_uuid}')
def get_single_remark_by_remark_uuid(remark_uuid: str, db: Session = Depends(get_db)):
    remark_db = crud.get_remark_by_remark_uuid(db=db, remark_uuid=remark_uuid)

    if not remark_db:
        raise HTTPException(
            status_code=500,
            detail="The comment doesn't exist."
        )

    temp_dict = {
        "id": remark_db.id,
        "remark_uuid": remark_db.remark_uuid,
        "post_uuid": remark_db.post_uuid,
        "user_uuid": remark_db.user_uuid,
        "user_name": remark_db.user_name,
        "content": remark_db.content,
        "date": remark_db.date,
        "avatar": dir_tool.get_avatar_file_url(dir_user_uuid=remark_db.user_uuid)[0]
    }

    return temp_dict


@Remark_router.get("/get/reply/{remark_uuid_for_get_reply}/{page}")
async def get_reply_by_remark_uuid(page: int,
                                   remark_uuid_for_get_reply: str,
                                   db: Session = Depends(get_db)):
    reply_from_db = crud.get_replies_by_remark_uuid(remark_uuid=remark_uuid_for_get_reply,
                                                    page=page, db=db)
    list_for_return: list[dict] = []
    for x in reply_from_db:
        temp_dict = {
            "id": x.id,
            "reply_to_remark_uuid": x.reply_to_remark_uuid,
            "reply_uuid": x.reply_uuid,
            "reply_to_user_name": x.reply_to_user_name,
            "reply_to_user_uuid": x.reply_to_user_uuid,
            "content": x.content,
            "user_uuid": x.user_uuid,
            "user_name": x.user_name,
            "avatar": dir_tool.get_avatar_file_url(dir_user_uuid=x.user_uuid)[0],
            "date": x.date
        }
        list_for_return.append(temp_dict)

    return list_for_return


@Remark_router.put("/update/inpost/{remark_uuid_for_update_remark}")
def update_remark_by_remark_uuid(remark_uuid_for_update_remark: str):
    pass


@Remark_router.delete("/delete/inpost/{remark_uuid_for_delete_remark}")
def delete_remark_by_remark_uuid(remark_uuid_for_delete_remark: str):
    pass
