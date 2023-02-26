# Request Body
from fastapi import UploadFile
from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    user_name: str
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
    user_name: str
    token: str

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    username: str
    disabled: Union[bool, None] = None


class PostCreate(BaseModel):
    post_title: str
    description: str

    class Config:
        orm_mode = True


class RemarkCreate(BaseModel):
    post_uuid: str
    user_name: str
    content: str
    depth: int
    remark_uuid: str
    reply_to: str

    class Config:
        orm_mode = True


class Posts(BaseModel):
    post_title: str
    description: str
    user_name: str
    post_uuid: str
    dots: int
    date: str

    class Config:
        orm_mode = True


class Remarks(BaseModel):
    post_uuid: str
    user_name: str
    content: str
    depth: int
    remark_uuid: str
    reply_to: str
    date: str

    class Config:
        orm_mode = True
