from fastapi import HTTPException
from ..utilities import token_tools as token_tool
from ..model import crud
from sqlalchemy.orm import Session


def auth_user_by_name(db: Session, token: str) -> str:
    """
    :param db:
    :param token:
    :return:
    """
    user_name_from_token: str = token_tool.get_user_name_by_token(token=token)
    if not user_name_from_token:
        raise HTTPException(
            status_code=400, detail="The user does not exist!")

    user_name_from_db = crud.get_user_by_name(db, user_name=user_name_from_token) if \
        crud.get_user_by_name(db, user_name=user_name_from_token) else \
        crud.get_admin_by_name(db, user_name=user_name_from_token)
    if not user_name_from_db:
        raise HTTPException(
            status_code=400, detail="The user does not exist!")

    return user_name_from_db.users_uuid


def get_user_uuid_by_name(db: Session, user_name: str) -> str | bool:
    user_uuid_from_db = crud.get_user_by_name(db, user_name=user_name)
    if not user_uuid_from_db:
        return False
    return user_uuid_from_db.users_uuid


def get_admin_uuid_by_name(db: Session, user_name: str) -> str | bool:
    admin_uuid_from_db = crud.get_admin_by_name(db, user_name=user_name)
    if not admin_uuid_from_db:
        return False

    return admin_uuid_from_db.users_uuid
