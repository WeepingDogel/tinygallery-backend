from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.oauth2scheme import oauth2Scheme
from app.dependencies.db import get_db
from ... import config
from app.utilities import admin_tool

admin_auth_router = APIRouter(
    prefix="/admin",
    tags=['Administration'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


@admin_auth_router.get("/admin_authentication")
def api_admin_auth(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)) -> dict:
    """
    Provide an authentication to administrators for entrance to the Management Web Page.
    :param token: The token of user
    :param db: Database Session.
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


@admin_auth_router.get('/get_all_users')
def get_all_users(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)) -> list:
    """
    Get the list of all users (Administrators are not included.)
    :param token: The admin token.
    :param db: Session of Database.
    :return: The list of users.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )
    return admin_tool.get_the_list_of_all_users(db=db)


@admin_auth_router.get('/get_all_admin')
def get_all_administrators(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)) -> list:
    """
    Get the list of all administrators (Administrators are not included.)
    :param token: The admin token
    :param db: Session of Database
    :return: The list of administrator.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )
    return admin_tool.get_the_list_of_all_admins(db=db)


@admin_auth_router.get('/get_all_posts')
def get_all_posts(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)) -> list:
    """
    Get the list of all posts (Administrators are not included.)
    :param token: The admin token
    :param db: Session of Database
    :return: The list of posts.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    return admin_tool.get_all_posts(db=db)


@admin_auth_router.get('/get_all_comments')
def get_all_comments(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the list of all comments (Administrators are not included.)
    :param token: The admin token
    :param db: Session of Database
    :return: The list of comments.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    return admin_tool.get_all_comments(db=db)


@admin_auth_router.get('/get_all_replies')
def get_all_replies(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the list of all replies (Administrators are not included.)
    :param token: The admin token
    :param db: Session of Database
    :return: The list of replies.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    return admin_tool.get_all_replies(db=db)


@admin_auth_router.put('/edit_user')
def edit_user(token: str = Depends(oauth2Scheme)):
    pass


@admin_auth_router.put('/block_user')
def block_a_user():
    pass


@admin_auth_router.delete('/delete_user')
def delete_a_user(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    pass
