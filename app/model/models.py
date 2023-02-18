from sqlalchemy import Boolean, Column, Integer, String
from ..db import Base



class User(Base):
    __tablename__ = 'USERS'
    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String, nullable=False,
                      sqlite_on_conflict_not_null='FAIL', unique=True)
    password = Column(String, nullable=False,
                      sqlite_on_conflict_not_null='FAIL')
    date = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    email = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    usersUUID = Column(String, nullable=False,
                       sqlite_on_conflict_not_null='FAIL', unique=True)


class Posts(Base):
    __tablename__ = "POSTS"
    id = Column(Integer, primary_key=True, index=True)
    postFilePath = Column(String, nullable=False,
                          sqlite_on_conflict_not_null='FAIL')
    postType = Column(String, nullable=False,
                       sqlite_on_conflict_not_null='FAIL')
    coverFileType = Column(String, nullable=False,
                           sqlite_on_conflict_not_null='Fail')
    postTitle = Column(String, nullable=False,
                       sqlite_on_conflict_not_null='FAIL')
    description = Column(String)
    dots = Column(Integer)
    shareNum = Column(Integer)
    nfsw = Column(Boolean)
    userName = Column(String, nullable=False,
                      sqlite_on_conflict_not_null='FAIL')
    date = Column(String, nullable=False, sqlite_on_conflict_not_null='FAIL')
    postUUID = Column(String, nullable=False,
                      sqlite_on_conflict_not_null='FAIL')
