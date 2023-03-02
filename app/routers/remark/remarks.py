from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from ...dependencies.db import get_db

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


@Remark_router.post("/create/inpost/{post_uuid_for_create_remark}")
def create_remark_for_post(post_uuid_for_create_remark: str):
    pass


@Remark_router.get("/get/inpost/{post_uuid_for_get_remark}")
def get_remark_in_post_by_postuuid(post_uuid_for_get_remark: str):
    pass


@Remark_router.put("/update/inpost/{remark_uuid_for_update_remark}")
def update_remark_by_remark_uuid(remark_uuid_for_update_remark: str):
    pass


@Remark_router.delete("/delete/inpost/{remark_uuid_for_delete_remark}")
def delete_remark_by_remark_uuid(remark_uuid_for_delete_remark: str):
    pass
