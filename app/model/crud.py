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


def db_create_post(db: Session,
                   user_name: str,
                   post_type: str,
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
        post_type=post_type,
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


