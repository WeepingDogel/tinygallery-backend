from sqlalchemy.orm import Session
import time, uuid
from . import models, schemas


def CreateUser(db: Session, user: schemas.User):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    userUUID = str(uuid.uuid4())
    db_user = models.User(
        userName = user.userName,
        password = user.password,
        email = user.email,
        date = date,
        usersUUID = userUUID
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def GetUserByName(db: Session, userName: str):
    return db.query(models.User).filter(models.User.userName == userName).first()