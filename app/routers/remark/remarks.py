from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Union
from ...model import schemas
from ...dependencies.db import get_db
from ...dependencies.oauth2scheme import oauth2Scheme
from ...model import crud
from ...utilities import token_tools

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


@Remark_router.get("/get/inpost/{post_uuid_for_get_remark}")
def get_remark_in_post_by_postuuid(post_uuid_for_get_remark: str,
                                   page: int):
    return {"page": page}


@Remark_router.put("/update/inpost/{remark_uuid_for_update_remark}")
def update_remark_by_remark_uuid(remark_uuid_for_update_remark: str):
    pass


@Remark_router.delete("/delete/inpost/{remark_uuid_for_delete_remark}")
def delete_remark_by_remark_uuid(remark_uuid_for_delete_remark: str):
    pass
