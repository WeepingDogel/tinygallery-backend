# Request Body
from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    userName: str
    password: str
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    userName: str
    token: str

    class Config:
        orm_mode = True


class User_Token(BaseModel):
    username: str
    disabled: Union[bool, None] = None


class Post_Create(BaseModel):
    postTitle: str
    description: str
    userName: str

    class Config:
        orm_mode = True


class Remark_Create(BaseModel):
    postUUID: str
    userName: str
    content: str
    depth: int
    remarkUUID: str
    replyTo: str

    class Config:
        orm_mode = True


class Posts(BaseModel):
    postTitle: str
    description: str
    userName: str
    postUUID: str
    dots: int
    date: str

    class Config:
        orm_mode = True


class Remarks(BaseModel):
    postUUID: str
    userName: str
    content: str
    depth: int
    remarkUUID: str
    replyTo: str
    date: str

    class Config:
        orm_mode = True
