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


class RemarkCreate(BaseModel):
    post_uuid: str
    content: str
    reply_to_remark_uuid: str
    reply_to_user: str
    reply_to_sub_remark_uuid: str

    class Config:
        orm_mode = True
