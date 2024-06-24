import time
import uuid
from typing import Type

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.utilities.hash_tool import get_password_hash
from . import models, schemas
from .models import Posts, Remarks, Replies, Likes, User
from .. import config
from ..utilities import userdata_tool


def create_user(db: Session, user: schemas.User):
    """
    :param db: The session of the database.
    :param user: The schemas of a user
    :return: The result of creating a user
    """
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user_uuid = str(uuid.uuid4())
    db_user = models.User(
        user_name=user.user_name,
        password=user.password,
        email=user.email,
        date=date,
        users_uuid=user_uuid
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_admin(db: Session, user: dict, password_hashed: str):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user_uuid = str(uuid.uuid4())
    db_admin = models.Admin(
        user_name=user['username'],
        password=password_hashed,
        email=user['email'],
        users_uuid=user_uuid,
        date=date
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)

    return db_admin


def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_admin_by_name(db: Session, user_name: str):
    return db.query(models.Admin).filter(models.Admin.user_name == user_name).first()


def get_user_by_uuid(db: Session, user_uuid: str):
    return db.query(models.User).filter(models.User.users_uuid == user_uuid).first()


def get_admin_by_uuid(db: Session, user_uuid: str):
    return db.query(models.Admin).filter(models.Admin.users_uuid == user_uuid).first()


# def update_user_name(db: Session, new_user_name: str):
#     pass


def db_create_post(db: Session,
                   user_name: str,
                   post_title: str,
                   description: str,
                   post_uuid: str,
                   is_nsfw: bool):
    date_db = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dots_db: int = 0
    share_num_db: int = 0

    db_post = models.Posts(
        user_name=user_name,
        post_title=post_title,
        post_uuid=post_uuid,
        description=description,
        date=date_db,
        nsfw=is_nsfw,
        dots=dots_db,
        share_num=share_num_db
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return True


def get_posts_by_page(db: Session, page: int) -> list[Type[Posts]]:
    post_limit = config.posts_limit
    page_db = (page - 1) * config.posts_limit
    return db.query(models.Posts) \
        .order_by(desc(models.Posts.date)) \
        .limit(post_limit).offset(page_db).all()


def get_single_post_by_uuid(db: Session, post_uuid: str) -> Type[Posts] | None:
    return db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid).first()


def remove_post_by_uuid(db: Session, post_uuid: str) -> bool:
    status: int = db.query(models.Posts). \
        filter(models.Posts.post_uuid == post_uuid). \
        delete("evaluate")
    if status == 0:
        return False
    db.commit()
    return True


def update_post_by_uuid(db: Session,
                        post_uuid: str,
                        is_nsfw: bool,
                        post_title: str,
                        post_description: str
                        ) -> bool:
    current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    status: int = db.query(models.Posts). \
        filter(models.Posts.post_uuid == post_uuid). \
        update(
        {
            "date": current_date,
            "post_title": post_title,
            "nsfw": is_nsfw,
            "description": post_description
        },
        synchronize_session="evaluate"
    )

    if status == 0:
        return False

    db.commit()

    return True


def get_all_posts_belong_to_user(db: Session, user_name: str, page: int) -> list[Type[Posts]]:
    single_page_posts_limit = config.posts_limit
    page_db = (page - 1) * config.posts_limit

    return db.query(models.Posts). \
        filter(models.Posts.user_name == user_name). \
        order_by(desc(models.Posts.date)). \
        limit(single_page_posts_limit).offset(page_db).all()


def create_remark(db: Session, remark_create: schemas.RemarkCreate, user_name: str):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    remark_uuid = str(uuid.uuid4())
    user_uuid = userdata_tool.get_user_uuid_by_name(db=db, user_name=user_name) if userdata_tool.get_user_uuid_by_name(
        db=db, user_name=user_name) else userdata_tool.get_admin_uuid_by_name(db=db, user_name=user_name)
    db_remark = models.Remarks(
        post_uuid=remark_create.post_uuid,
        user_uuid=user_uuid,
        user_name=user_name,
        remark_uuid=remark_uuid,
        content=remark_create.content,
        date=date
    )
    db.add(db_remark)
    db.commit()
    db.refresh(db_remark)
    return True


def create_reply(db: Session, reply_create: schemas.ReplyCreate, user_name: str):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    reply_uuid = str(uuid.uuid4())
    user_uuid = userdata_tool.get_user_uuid_by_name(db=db, user_name=user_name) if userdata_tool.get_user_uuid_by_name(
        db=db, user_name=user_name) else userdata_tool.get_admin_uuid_by_name(db=db, user_name=user_name)
    reply_to_user_uuid = userdata_tool.get_user_uuid_by_name(db=db, user_name=reply_create.reply_to_user_name)
    db_reply = models.Replies(
        reply_to_remark_uuid=reply_create.reply_to_remark_uuid,
        reply_uuid=reply_uuid,
        reply_to_user_name=reply_create.reply_to_user_name,
        reply_to_user_uuid=reply_to_user_uuid,
        content=reply_create.content,
        user_uuid=user_uuid,
        user_name=user_name,
        date=date
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return True


def get_remarks_by_post_uuid(db: Session, post_uuid: str, page: int) -> list[Type[Remarks]]:
    remark_limit = config.remark_limit
    remark_db = (page - 1) * config.remark_limit
    return db.query(models.Remarks).filter(models.Remarks.post_uuid == post_uuid) \
        .order_by(desc(models.Remarks.date)) \
        .limit(remark_limit).offset(remark_db).all()


def get_remark_by_remark_uuid(db: Session, remark_uuid: str) -> Type[Remarks] | None:
    return db.query(models.Remarks).filter(models.Remarks.remark_uuid == remark_uuid).first()


def get_replies_by_remark_uuid(db: Session, remark_uuid: str, page: int) -> list[Type[Replies]]:
    reply_limit = config.reply_limit
    remark_db = (page - 1) * config.reply_limit
    return db.query(models.Replies).filter(models.Replies.reply_to_remark_uuid == remark_uuid) \
        .order_by(desc(models.Replies.date)) \
        .limit(reply_limit).offset(remark_db).all()


def get_like_status_from_database(db: Session, post_uuid: str, user_name: str) -> Type[Likes] | None:
    return db.query(models.Likes).filter(models.Likes.post_uuid == post_uuid, models.Likes.user_name == user_name) \
        .first()


def write_like_status_in_database(db: Session, post_uuid: str, user_name: str) -> bool:
    db_posts = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid)
    origin_num_of_likes = db_posts.first().dots
    current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not get_like_status_from_database(db=db, post_uuid=post_uuid, user_name=user_name):
        user_uuid = userdata_tool.get_user_uuid_by_name(db=db,
                                                        user_name=user_name) if userdata_tool.get_user_uuid_by_name(
            db=db, user_name=user_name) else userdata_tool.get_admin_uuid_by_name(db=db, user_name=user_name)

        if not user_uuid:
            return False

        db_like = models.Likes(
            post_uuid=post_uuid,
            user_name=user_name,
            user_uuid=user_uuid,
            liked=True,
            date=current_date
        )
        status: int = db_posts.update(
            {
                "dots": origin_num_of_likes + 1
            },
            synchronize_session="fetch"
        )

        if status == 0:
            return False

        db.add(db_like)
        db.commit()
        db.refresh(db_like)
        return True
    else:
        db_like = db.query(models.Likes) \
            .filter(models.Likes.post_uuid == post_uuid, models.Likes.user_name == user_name)
        if not db_like.first().liked:
            status_like: int = db_like.update(
                {
                    "liked": True,
                    "date": current_date
                },
                synchronize_session="fetch"
            )
            status_post: int = db_posts.update(
                {
                    "dots": origin_num_of_likes + 1
                },
                synchronize_session="fetch"
            )
            if status_like == 0:
                return False
            if status_post == 0:
                return False

            db.commit()
            return True


def cancel_like_status_in_database(db: Session, post_uuid: str, user_name: str) -> bool:
    db_posts = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid)
    origin_num_of_likes = db_posts.first().dots
    db_like = db.query(models.Likes) \
        .filter(models.Likes.post_uuid == post_uuid, models.Likes.user_name == user_name)
    current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not db_like:
        return False

    status_like: int = db_like.update(
        {
            "liked": False,
            "date": current_date
        },
        synchronize_session="fetch"
    )

    status_post: int = db_posts.update(
        {
            "dots": origin_num_of_likes - 1
        },
        synchronize_session="fetch"
    )

    if status_like == 0:
        return False

    if status_post == 0:
        return False

    db.commit()

    return True


def get_user_quantity(db: Session):
    db_users_num = db.query(func.count()).select_from(models.User).scalar() + \
                   db.query(func.count()).select_from(models.Admin).scalar()
    return db_users_num


def get_posts_quantity(db: Session):
    db_posts_num = db.query(func.count()).select_from(models.Posts).scalar()
    return db_posts_num


def get_comments_quantity(db: Session):
    db_comments_num = db.query(func.count()).select_from(models.Remarks).scalar() \
                      + db.query(func.count()).select_from(models.Replies).scalar()
    return db_comments_num


# Functions below are only prepared for administrators.

def get_all_users(db: Session) -> list[Type[User]]:
    """
    Query the list of all users.
    :param db: Session of the database.
    :return: The list of all users.
    """

    return db.query(models.User).all()


def get_all_admins(db: Session) -> list:
    """
    Query the list of all administrators.
    :param db: Session of the database
    :return: The list of all administrators
    """

    return db.query(models.Admin).all()


def get_all_posts(db: Session) -> list:
    """
    Query the list of all posts.
    :param db: Session of the database.
    :return: The list of all posts.
    """

    return db.query(models.Posts).all()


def get_all_comments(db: Session) -> list:
    """
    Query the list of all comments.
    :param db: Session of the database.
    :return: The list of all comments.
    """

    return db.query(models.Remarks).all()


def get_all_replies(db: Session) -> list:
    """
    Query the list of all replies.
    :param db: Session of the database.
    :return: The list of all replies.
    """

    return db.query(models.Replies).all()


def get_data_of_a_user(db: Session, user_uuid: str) -> dict:
    """
    Get data of a user by uuid, return a dict.
    :param user_uuid: The uuid of the user.
    :param db: Session of the database.
    :return: A list of data.
    """
    return db.query(models.User).filter(models.User.users_uuid == user_uuid).first()


def get_data_of_a_post(db: Session, post_uuid: str) -> dict:
    """
    Get data of a post by uuid, return a List.
    :param db: Session of the database.
    :param post_uuid: THe uuid of the post.
    :return: A list of data.
    """

    return db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid).first()


def update_data_of_a_user(user_manage: schemas.UserManage, db: Session):
    """
    Update data of a user by uuid, return a Bool.
    :param user_manage:
    :param db: Session of the database.
    :return: If success, return True.Otherwise, return the false.
    """

    db_update_user = db.query(models.User).filter(models.User.users_uuid == user_manage.user_uuid)

    if db_update_user.first().user_name != user_manage.user_name:
        status: int = db_update_user.update(
            {
                'user_name': user_manage.user_name
            },
            synchronize_session="evaluate"
        )

        if status == 0:
            return False

        db.commit()

    if db_update_user.first().password != user_manage.password:
        hashed_password = get_password_hash(password=user_manage.password)
        status: int = db_update_user.update(
            {
                'password': hashed_password
            },
            synchronize_session="evaluate"
        )

        if status == 0:
            return False

        db.commit()

    if db_update_user.first().email != user_manage.email:
        status: int = db_update_user.update(
            {
                "email": user_manage.email
            },
            synchronize_session="evaluate"
        )

        if status == 0:
            return False

        db.commit()

    if db_update_user.first().date != user_manage.date:
        status: int = db_update_user.update(
            {
                'date': user_manage.date
            },
            synchronize_session="evaluate"
        )

        if status == 0:
            return False

        db.commit()

    return True
