import time
import uuid
from typing import Type

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.utilities.hash_tool import get_password_hash
from . import models, schemas
from .models import Posts, Remarks, Replies, Likes, User, Admin
from .. import config
from ..utilities import userdata_tool
from datetime import datetime
from ..utilities.image_tools import generate_default_avatar, generate_user_avatar  # Update this import
import base64
from io import BytesIO
from PIL import Image
from ..utilities import dir_tool
from fastapi import UploadFile


def create_user(db: Session, user: schemas.User):
    """
    :param db: The session of the database.
    :param user: The schemas of a user
    :return: The result of creating a user
    """
    date = datetime.utcnow()
    user_uuid = str(uuid.uuid4())
    db_user = models.User(
        user_name=user.user_name,
        password=get_password_hash(user.password),
        email=user.email,
        date=date,
        users_uuid=user_uuid
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    generate_default_avatar(user_uuid)
    return db_user


def create_admin(db: Session, user: dict, password_hashed: str):
    date = datetime.utcnow()
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
    generate_default_avatar(user_uuid)
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
    date_db = datetime.utcnow()  # Use datetime.utcnow() instead of a string
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


def get_posts_by_page(db: Session, page: int):
    return db.query(models.Posts).order_by(desc(models.Posts.date)).offset((page - 1) * config.posts_limit).limit(config.posts_limit).all()


def get_single_post_by_uuid(db: Session, post_uuid: str):
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


def get_all_posts_belong_to_user(db: Session, user_name: str, page: int):
    return db.query(models.Posts).filter(models.Posts.user_name == user_name).order_by(desc(models.Posts.date)).offset((page - 1) * config.posts_limit).limit(config.posts_limit).all()


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


def get_all_admins(db: Session) -> list[Admin]:
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

# Admin User Management

def admin_get_all_users(db: Session):
    users = db.query(models.User).all()
    for user in users:
        avatar_urls = dir_tool.get_avatar_file_url(user.users_uuid)
        setattr(user, 'avatar', avatar_urls[0])  # Use the full-size avatar URL
    return users

def admin_create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    user_uuid = str(uuid.uuid4())
    db_user = models.User(
        user_name=user.user_name,
        password=hashed_password,
        email=user.email,
        date=datetime.utcnow(),
        users_uuid=user_uuid
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    generate_default_avatar(user_uuid)
    return db_user

def admin_update_user(db: Session, user_uuid: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.users_uuid == user_uuid).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['password'] = get_password_hash(update_data['password'])
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        
        # Add avatar URL to the user object
        avatar_urls = dir_tool.get_avatar_file_url(user_uuid)
        setattr(db_user, 'avatar', avatar_urls[0])  # Use the full-size avatar URL
    return db_user

def admin_delete_user(db: Session, user_uuid: str):
    db_user = db.query(models.User).filter(models.User.users_uuid == user_uuid).first()
    if db_user:
        posts = db.query(models.Posts).filter(models.Posts.user_name == db_user.user_name).all()
        for post in posts:
            db.query(models.Remarks).filter(models.Remarks.post_uuid == post.post_uuid).delete(synchronize_session=False)
            db.query(models.Replies).filter(models.Replies.reply_to_remark_uuid.in_(
                db.query(models.Remarks.remark_uuid).filter(models.Remarks.post_uuid == post.post_uuid)
            )).delete(synchronize_session=False)
            db.delete(post)
        
        db.query(models.Remarks).filter(models.Remarks.user_uuid == user_uuid).delete(synchronize_session=False)
        db.query(models.Replies).filter(models.Replies.user_uuid == user_uuid).delete(synchronize_session=False)
        db.query(models.Likes).filter(models.Likes.user_uuid == user_uuid).delete(synchronize_session=False)
        
        db.delete(db_user)
        db.commit()
        return True
    return False

def admin_get_user_by_uuid(db: Session, user_uuid: str):
    user = db.query(models.User).filter(models.User.users_uuid == user_uuid).first()
    if user:
        user_dict = user.__dict__
        avatar_urls = dir_tool.get_avatar_file_url(user_uuid)
        user_dict['avatar'] = avatar_urls[0]  # Use the full-size avatar URL
        return user_dict
    return None

# Admin Post Management

def admin_get_all_posts(db: Session):
    return db.query(models.Posts).all()

def admin_create_post(db: Session, post: schemas.PostCreate, user_name: str):
    db_post = models.Posts(
        user_name=user_name,
        post_title=post.post_title,
        post_uuid=str(uuid.uuid4()),
        description=post.description,
        nsfw=post.nsfw,
        date=datetime.utcnow(),
        dots=0,
        share_num=0
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def admin_update_post(db: Session, post_uuid: str, post: schemas.PostUpdate):
    db_post = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid).first()
    if db_post:
        update_data = post.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
        
        # Add image_link to the response
        post_dict = db_post.__dict__
        post_dict['image_link'] = dir_tool.get_post_image_link(post_uuid)
        return post_dict
    return None

def admin_delete_post(db: Session, post_uuid: str):
    db_post = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid).first()
    if db_post:
        db.query(models.Remarks).filter(models.Remarks.post_uuid == post_uuid).delete(synchronize_session=False)
        db.query(models.Replies).filter(models.Replies.reply_to_remark_uuid.in_(
            db.query(models.Remarks.remark_uuid).filter(models.Remarks.post_uuid == post_uuid)
        )).delete(synchronize_session=False)
        db.query(models.Likes).filter(models.Likes.post_uuid == post_uuid).delete(synchronize_session=False)
        db.delete(db_post)
        db.commit()
        return True
    return False

# Admin Comment Management

def admin_get_all_comments(db: Session):
    return db.query(models.Remarks).all()

def admin_create_comment(db: Session, comment: schemas.CommentCreate, user_name: str):
    user = get_user_by_name(db, user_name)
    if not user:
        return None
    db_comment = models.Remarks(
        post_uuid=comment.post_uuid,
        user_name=user_name,
        user_uuid=user.users_uuid,
        remark_uuid=str(uuid.uuid4()),
        content=comment.content,
        date=datetime.utcnow()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def admin_update_comment(db: Session, comment_uuid: str, comment: schemas.CommentUpdate):
    db_comment = db.query(models.Remarks).filter(models.Remarks.remark_uuid == comment_uuid).first()
    if db_comment:
        update_data = comment.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
    return db_comment

def admin_delete_comment(db: Session, remark_uuid: str):
    db_comment = db.query(models.Remarks).filter(models.Remarks.remark_uuid == remark_uuid).first()
    if db_comment:
        db.query(models.Replies).filter(models.Replies.reply_to_remark_uuid == remark_uuid).delete(synchronize_session=False)
        db.delete(db_comment)
        db.commit()
        return True
    return False

# Additional Admin Functions

def admin_get_user_activity(db: Session, user_uuid: str) -> schemas.UserActivity:
    user = db.query(models.User).filter(models.User.users_uuid == user_uuid).first()
    if user:
        user_posts = db.query(models.Posts).filter(models.Posts.user_name == user.user_name).count()
        user_comments = db.query(models.Remarks).filter(models.Remarks.user_uuid == user_uuid).count()
        return schemas.UserActivity(posts=user_posts, comments=user_comments)
    return None

def admin_get_post_statistics(db: Session, post_uuid: str) -> schemas.PostStatistics:
    post = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid).first()
    if post:
        comments_count = db.query(models.Remarks).filter(models.Remarks.post_uuid == post_uuid).count()
        return schemas.PostStatistics(likes=post.dots, comments=comments_count, shares=post.share_num)
    return None

def admin_update_user_avatar(db: Session, user_uuid: str, avatar: UploadFile):
    user = db.query(models.User).filter(models.User.users_uuid == user_uuid).first()
    if not user:
        return None
    
    contents = avatar.file.read()
    image = Image.open(BytesIO(contents))
    
    generate_user_avatar(user_uuid, image)
    
    avatar_url = dir_tool.get_avatar_file_url(user_uuid)[0]
    setattr(user, 'avatar', avatar_url)
    
    return user

# Add this new function

def admin_get_post_by_uuid(db: Session, post_uuid: str):
    post = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid).first()
    if post:
        post_dict = post.__dict__
        post_dict['image_link'] = dir_tool.get_post_image_link(post_uuid)
        return post_dict
    return None

def admin_get_comment_by_uuid(db: Session, comment_uuid: str):
    comment = db.query(models.Remarks).filter(models.Remarks.remark_uuid == comment_uuid).first()
    if comment:
        return comment
    return None