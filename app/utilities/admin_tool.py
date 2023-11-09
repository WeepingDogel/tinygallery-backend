import pandas
from fastapi import HTTPException
from .hash_tool import get_password_hash
from .json_config_reader import read_admin_list
from app.model.crud import create_admin, get_admin_by_name, get_all_users, \
    get_all_posts, get_all_admins, get_all_comments, get_all_replies, get_data_of_a_post, get_data_of_a_user, \
    update_data_of_a_user
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.dependencies.db import engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import ADMIN_LIST
from app.utilities.token_tools import get_user_name_by_token
from app.model import schemas
from objtyping import to_primitive
import pandas as pd
import json

get_db = sessionmaker(bind=engine)


def create_admin_users(db: Session = get_db(), admin_list: list = read_admin_list(ADMIN_LIST)) -> bool:
    """
    :param db: The Database Session of SQLAlchemy.
    :param admin_list: The list of usernames to create administrators.
    :return:
    """
    if not admin_list:
        raise ValueError("Admin list is empty")
    num_created = 0
    for admin in admin_list:
        if not get_admin_by_name(user_name=admin['username'], db=db):
            try:
                create_admin(user=admin, db=db, password_hashed=get_password_hash(admin['password']))
            except SQLAlchemyError:
                print("SQLAlchemy Error!")
                return False
            except OperationalError:
                print("[Error] User has already existed:" + admin['username'])
            finally:
                print("[OK] Admin created successfully:" + admin['username'])
    if num_created > 0:
        return True
    else:
        return False


def admin_identification_check(token: str, db: Session):
    user_name = get_user_name_by_token(token=token)
    db_admin = get_admin_by_name(db=db, user_name=user_name)
    if not db_admin:
        return False
    return db_admin


def get_the_list_of_all_users(db: Session) -> list:
    """
    Get the list of all users.
    :param db: Session of a database.
    :return: A list of users.
    """
    db_all_users = get_all_users(db=db)
    return db_all_users


def get_the_list_of_all_admins(db: Session) -> list:
    """
    Get the list of all administrators.
    :param db: Session of a database.
    :return: A list of administrators.
    """
    db_all_admins = get_all_admins(db=db)

    return db_all_admins


def get_the_list_of_all_posts(db: Session) -> list:
    """
    Get the list of all posts.
    :param db: Session of a database.
    :return: A list of posts
    """

    db_all_posts = get_all_posts(db=db)
    return db_all_posts


def get_the_list_of_all_comments(db: Session) -> list:
    """
    Get the list of all comments.
    :param db: Session of a database.
    :return: A list of comments.
    """

    db_all_comments = get_all_comments(db=db)
    return db_all_comments


def get_the_list_of_all_replies(db: Session) -> list:
    """
    Get the list of all comments.
    :param db: Session of a database.
    :return: A list of comments.
    """
    db_all_replies = get_all_replies(db=db)
    return db_all_replies


def edit_the_user(user_manage: schemas.UserManage, db: Session):
    """
    Edit a user by providing new information.
    :param user_manage: The request body of the new data.
    :param db: Session of the database.
    :return: The status of the update.
    """

    if update_data_of_a_user(user_manage=user_manage, db=db):
        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Database Error, update user data failed."
        )


def get_the_tendency_data(db: Session):
    """
    Get the data of users' tendency.
    :param db: The Session of database.
    :return: The data of users' tendency.
    """

    data_all_users = pd.read_json(json.dumps(to_primitive(get_all_users(db=db))))
    data_all_posts = pd.read_json(json.dumps(to_primitive(get_all_posts(db=db))))
    data_all_comments = pd.read_json(json.dumps(to_primitive(get_all_comments(db=db))))
    data_all_replies = pd.read_json(json.dumps(to_primitive(get_all_replies(db=db))))
    data_all_users['date'] = pd.to_datetime(data_all_users['date']).dt.date
    data_all_posts['date'] = pd.to_datetime(data_all_posts['date']).dt.date
    data_all_comments['date'] = pd.to_datetime(data_all_comments['date']).dt.date
    data_all_replies['date'] = pd.to_datetime(data_all_replies['date']).dt.date
    count_users = data_all_users.groupby('date')['users_uuid'].count()
    count_posts = data_all_posts.groupby('date')['post_uuid'].count()
    count_comments = data_all_comments.groupby('date')['remark_uuid'].count()
    count_replies = data_all_replies.groupby('date')['reply_uuid'].count()
    data_final = pd.DataFrame({'users': count_users, 'posts': count_posts, 'comments': count_comments,
                               'replies': count_replies})
    data_final = data_final.fillna(0)
    # print(data_final)
    return data_final


def get_the_toplist_data(db: Session):
    """
    Get and analyze the data of the toplist from database.
    :param db: Session of the database.
    :return: The final data to output.
    """

    # Get the original data from database and convert to json.
    data_all_posts_original = pd.read_json(json.dumps(to_primitive(get_all_posts(db=db))))
    data_posts_rank = data_all_posts_original.sort_values('dots', ascending=False)[['post_title', 'dots']]

    return data_posts_rank


def get_the_data_of_a_single_user(db: Session, user_uuid: str):
    """
    Get the data of a single user by uuid.
    :param db: The session of database.
    :param user_uuid: The uuid of the user.
    :return: A JSON data of the user's properties.
    """
    db_user = get_data_of_a_user(db=db, user_uuid=user_uuid)

    return db_user


def get_the_data_of_a_single_post(db: Session, post_uuid: str):
    """
    Get the data of a single post by uuid.
    :param db: The Session of database.
    :param post_uuid: the uuid of the post.
    :return: A JSON datab of the post's properties.
    """

    db_post = get_data_of_a_post(db=db, post_uuid=post_uuid)

    return db_post
