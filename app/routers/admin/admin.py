import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.oauth2scheme import oauth2Scheme
from app.dependencies.db import get_db
from ... import config
from app.utilities import admin_tool
from app.model import schemas
from pyecharts.charts import Line
from pyecharts.charts import Funnel
from pyecharts import options as opts

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


@admin_auth_router.get('/get_single_user')
def get_single_user(user_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the data of a single user by providing an uuid.
    :param user_uuid: The uuid of the user to query.
    :param token: The token of administrator to identify.
    :param db: The Session of the database.
    :return: A json type data of the user to query.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    return admin_tool.get_data_of_a_user(user_uuid=user_uuid, db=db)


@admin_auth_router.put('/edit_user')
def edit_user(user_manage: schemas.UserManage, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Edit a user.
    :param user_manage: The data of the user to be updated.
    :param token: The token of administrator.
    :param db: The Session of Database.
    :return: The result of editing a user.
    """
    auth__admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth__admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    # return 'Test'
    return admin_tool.edit_the_user(user_manage=user_manage, db=db)


@admin_auth_router.put('/block_user')
def block_a_user(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Block a user.
    :param token: The token of administrator.
    :param db: The Session of Database.
    :return: The result of blocking a user.
    """
    pass


@admin_auth_router.delete('/delete_user')
def delete_a_user(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Delete a user.
    :param token: The token of administrator.
    :param db: The Session of Database.
    :return: The result of deleting a user.
    """
    pass


@admin_auth_router.get('/user_tendency_addition')
def get_user_tendency(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the tendency of the users in 360 days.
    :param token: The token of the administrator.
    :param db: The Session of the database.
    :return: The data of the users' tendency.
    """

    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    data_final = admin_tool.get_the_tendency_data(db=db)
    x_date = data_final.index.to_list()
    y_user = data_final['users'].to_list()
    y_posts = data_final['posts'].to_list()
    y_comments = data_final['comments'].to_list()
    y_replies = data_final['replies'].to_list()
    chart_tendency = (
        Line()
        .add_xaxis(x_date)
        .add_yaxis('Users', y_user, is_smooth=True)
        .add_yaxis('Posts', y_posts, is_smooth=True)
        .add_yaxis('Comments', y_comments, is_smooth=True)
        .add_yaxis('Replies', y_replies, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Data tendency"))
    )
    #
    return chart_tendency.dump_options_with_quotes()


@admin_auth_router.get('/posts_toplist')
def get_posts_tops(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the toplist of the posts by likes.
    :param token: The token of the administrator.
    :param db: The Session of the database.
    :return: The data of the users' tendency.
    """
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )

    data_final = admin_tool.get_the_toplist_data(db=db)
    x_axis = data_final['post_title'].to_list()
    y_axis = data_final['dots'].to_list()
    # print(x_axis, y_axis)
    chart_toplist = (
        Funnel()
        .add('Rank by Likes', [list(z) for z in zip(x_axis, y_axis)])
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="Rank"))
    )

    return chart_toplist.dump_options_with_quotes()
