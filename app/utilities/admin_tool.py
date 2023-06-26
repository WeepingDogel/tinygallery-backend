from fastapi import HTTPException
from .hash_tool import get_password_hash
from .json_config_reader import read_admin_list
from app.model.crud import create_admin, get_admin_by_name, get_all_users, \
    get_all_posts, get_all_admins, get_all_comments, get_all_replies
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.dependencies.db import engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import ADMIN_LIST
from app.utilities.token_tools import get_user_name_by_token

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
