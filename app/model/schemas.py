# Request Body
from typing import Union, Optional
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    user_name: str
    password: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True  # This allows using from_orm


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


class Admin(BaseModel):
    user_name: str
    email: str
    date: str
    users_uuid: str

    class Config:
        orm_mode = True
        from_attributes = True  # Add this line


class PostCreate(BaseModel):
    post_title: str
    description: str
    nsfw: bool

    class Config:
        orm_mode = True
        from_attributes = True


class PostUpdate(BaseModel):
    post_title: Optional[str] = None
    description: Optional[str] = None
    nsfw: Optional[bool] = None

    class Config:
        orm_mode = True
        from_attributes = True


class RemarkUpdate(BaseModel):
    content: str

    class Config:
        orm_mode = True
        from_attributes = True


class PostStatistics(BaseModel):
    likes: int
    comments: int
    shares: int

    class Config:
        orm_mode = True
        from_attributes = True


class UserActivity(BaseModel):
    posts: int
    comments: int

    class Config:
        orm_mode = True
        from_attributes = True


class UserAdminView(BaseModel):
    id: int
    users_uuid: str
    user_name: str
    email: str
    date: datetime
    avatar: str

    class Config:
        orm_mode = True
        from_attributes = True


class PostAdminView(BaseModel):
    id: int
    post_uuid: str
    user_name: str
    post_title: str
    description: str
    nsfw: bool
    dots: int
    share_num: int
    date: datetime
    image_link: str

    class Config:
        orm_mode = True
        from_attributes = True


class CommentAdminView(BaseModel):
    id: int
    remark_uuid: str
    post_uuid: str
    user_name: str
    content: str
    date: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class UserCreate(BaseModel):
    user_name: str
    password: str
    email: str


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class CommentCreate(BaseModel):
    post_uuid: str
    content: str


class CommentUpdate(BaseModel):
    content: Optional[str] = None


# Add this new schema
class AvatarUpdate(BaseModel):
    user_uuid: str

    class Config:
        from_attributes = True
