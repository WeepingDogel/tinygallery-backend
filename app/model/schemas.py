# Request Body
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

    class Config:
        orm_mode = True


class ReplyCreate(BaseModel):
    reply_to_remark_uuid: str
    reply_to_user_name: str
    content: str

    class Config:
        orm_mode = True


class UserManage(BaseModel):
    user_uuid: str
    user_name: str
    password: str
    email: str
    date: str

    class Config:
        orm_mode = True
