from sqlalchemy import Boolean, Column, Integer, String
from app.dependencies.db import Base


class User(Base):
    __tablename__ = 'USERS'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False,
                       sqlite_on_conflict_not_null='FAIL', unique=True)
    password = Column(String, nullable=False,
                      sqlite_on_conflict_not_null='FAIL')
    date = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    email = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    users_uuid = Column(String, nullable=False,
                        sqlite_on_conflict_not_null='FAIL', unique=True)


class Posts(Base):
    __tablename__ = "POSTS"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False,
                       sqlite_on_conflict_not_null='FAIL')
    post_title = Column(String, nullable=False,
                        sqlite_on_conflict_not_null='FAIL')
    nsfw = Column(Boolean)
    description = Column(String)
    dots = Column(Integer)
    share_num = Column(Integer)
    date = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    post_uuid = Column(String, nullable=False,
                       sqlite_on_conflict_not_null='FAIL')


class Remarks(Base):
    __tablename__ = "REMARKS"
    id = Column(Integer, primary_key=True, index=True)
    remark_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL', unique=True)
    post_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    user_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    user_name = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    content = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    date = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')


class Replies(Base):
    __tablename__ = "REPLIES"
    id = Column(Integer, primary_key=True, index=True)
    reply_to_remark_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    reply_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL', unique=True)
    reply_to_user_name = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    reply_to_user_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    content = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    user_uuid = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    user_name = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    date = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
