import time
import uuid

from sqlalchemy.orm import Session

from . import models, schemas


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


def db_create_post(user_name: str,
                   post_title: str,
                   description: str,
                   is_nsfw: bool, ):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db_post = models.Posts(
        user_name=user_name,
        postTitle=post_title,
        description=description,
        date=date,
        nsfw=is_nsfw,
        post_uuid=str(uuid.uuid4()),
        share_num=0,
        dots=0,

    )
