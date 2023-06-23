from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.oauth2scheme import oauth2Scheme
from app.dependencies.db import get_db
from ... import config
from app.utilities import admin_tool


admin_auth_router = APIRouter(
    prefix="/user",
    tags=['Administration'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


@admin_auth_router.get("/admin_authentication")
def api_admin_auth(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Provide an authentication to administrators for entrance to the Management Web Page.
    :param token: The token of user
    :param db: Database Session
    :return:
    """
    auth_admin = admin_tool.admin_identification_check(db=db, token=token)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )
    return {
        "Code": 200,
        "Administrator": auth_admin.user_name,
        "Status": "Permission Accessed!"
    }
