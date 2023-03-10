import time
import uuid

from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models, schemas
from .models import Posts
from .. import config


def create_user(db: Session, user: schemas.User):
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


def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def update_user_name(db: Session, new_user_name: str):
    pass


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


def get_posts_by_page(db: Session, page: int) -> list[Posts]:
    post_limit = config.posts_limit
    page_db = (page - 1) * config.posts_limit
    return db.query(models.Posts) \
        .order_by(desc(models.Posts.date)) \
        .limit(post_limit).offset(page_db).all()


def get_single_post_by_uuid(db: Session, post_uuid: str) -> list[Posts]:
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


def get_all_posts_belong_to_user(db: Session, user_name: str, page: int) -> list[Posts]:
    single_page_posts_limit = config.posts_limit
    page_db = (page - 1) * config.posts_limit

    return db.query(models.Posts).\
        filter(models.Posts.user_name == user_name).\
        order_by(desc(models.Posts.date)).\
        limit(single_page_posts_limit).offset(page_db).all()
