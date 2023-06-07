import time
import uuid

from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from ..utilities import userdata_tool
from . import models, schemas
from .models import Posts, Remarks, Replies, Likes
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

    return db.query(models.Posts). \
        filter(models.Posts.user_name == user_name). \
        order_by(desc(models.Posts.date)). \
        limit(single_page_posts_limit).offset(page_db).all()


def create_remark(db: Session, remark_create: schemas.RemarkCreate, user_name: str):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    remark_uuid = str(uuid.uuid4())
    user_uuid = userdata_tool.get_user_uuid_by_name(db=db, user_name=user_name)
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
    user_uuid = userdata_tool.get_user_uuid_by_name(db=db, user_name=user_name)
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


def get_remarks_by_post_uuid(db: Session, post_uuid: str, page: int) -> list[Remarks]:
    remark_limit = config.remark_limit
    remark_db = (page - 1) * config.remark_limit
    return db.query(models.Remarks).filter(models.Remarks.post_uuid == post_uuid) \
        .order_by(desc(models.Remarks.date)) \
        .limit(remark_limit).offset(remark_db).all()


def get_remark_by_remark_uuid(db: Session, remark_uuid: str) -> list[Remarks]:
    return db.query(models.Remarks).filter(models.Remarks.remark_uuid == remark_uuid).first()


def get_replies_by_remark_uuid(db: Session, remark_uuid: str, page: int) -> list[Replies]:
    reply_limit = config.reply_limit
    remark_db = (page - 1) * config.reply_limit
    return db.query(models.Replies).filter(models.Replies.reply_to_remark_uuid == remark_uuid) \
        .order_by(desc(models.Replies.date)) \
        .limit(reply_limit).offset(remark_db).all()


def get_like_status_from_database(db: Session, post_uuid: str, user_name: str) -> Likes:
    return db.query(models.Likes).filter(models.Likes.post_uuid == post_uuid, models.Likes.user_name == user_name) \
        .first()


def write_like_status_in_database(db: Session, post_uuid: str, user_name: str) -> bool:
    db_posts = db.query(models.Posts).filter(models.Posts.post_uuid == post_uuid)
    origin_num_of_likes = db_posts.first().dots
    current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not get_like_status_from_database(db=db, post_uuid=post_uuid, user_name=user_name):
        user_uuid = userdata_tool.get_user_uuid_by_name(db=db, user_name=user_name)
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
    db_users_num = db.query(func.count()).select_from(models.User).scalar()
    return db_users_num


def get_posts_quantity(db: Session):
    db_posts_num = db.query(func.count()).select_from(models.Posts).scalar()
    return db_posts_num


def get_comments_quantity(db: Session):
    db_comments_num = db.query(func.count()).select_from(models.Remarks).scalar()
    return db_comments_num
