# Importing necessary libraries
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from app.utilities.hash_tool import verify_password, get_password_hash
# Importing modules from application
from app.utilities.image_tools import generate_default_avatar
from app.utilities.userdata_tool import get_user_uuid_by_name
from app.model import schemas
from app.model import crud
from app.dependencies.db import get_db
from app import config
from app.dependencies.oauth2scheme import oauth2Scheme
from app.utilities.token_tools import get_user_name_by_token, create_access_token, authenticate_user, authenticate_admin

# Defining router
userAuthRouter = APIRouter(
    prefix="/user",
    tags=['User'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


# Route for user registration
@userAuthRouter.post("/register")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # 检查密码长度
    if len(user.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters long"
        )
    
    db_user = crud.get_user_by_name(db, user_name=user.user_name)
    db_admin = crud.get_admin_by_name(db, user_name=user.user_name)
    
    # 检查用户名长度
    if len(user.user_name) < 3:
        raise HTTPException(
            status_code=400,
            detail="Username must be at least 3 characters long"
        )

    if user.user_name == "" or user.password == "" or user.email == "":
        raise HTTPException(
            status_code=400, 
            detail="Username, password and email can't be empty."
        )

    if db_user or db_admin:
        raise HTTPException(
            status_code=400, 
            detail="Username has already existed!"
        )

    try:
        # 对原始密码进行一次哈希
        user.password = get_password_hash(user.password)
        # 直接创建用户，不要再次哈希密码
        db_user = schemas.UserInDB(
            user_name=user.user_name,
            password=user.password,  # 已经哈希过的密码
            email=user.email
        )
        crud.create_user(db=db, user=db_user)
        generate_default_avatar(user_uuid=get_user_uuid_by_name(user_name=user.user_name, db=db))
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )


# Route for user login
@userAuthRouter.post("/token")
async def user_login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        print(f"Login attempt for user: {form_data.username}")
        
        # 检查用户是否存在
        db_user = crud.get_user_by_name(db, user_name=form_data.username)
        if db_user:
            is_valid = verify_password(form_data.password, db_user.password)
            if is_valid:
                access_token = create_access_token(
                    data={"sub": form_data.username, "type": "user"},
                    expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                print(f"Login successful for user: {form_data.username}")
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_type": "user"
                }
            print(f"Password verification failed for user: {form_data.username}")
        
        # 检查管理员
        db_admin = crud.get_admin_by_name(db, user_name=form_data.username)
        if db_admin:
            is_valid = verify_password(form_data.password, db_admin.password)
            if is_valid:
                access_token = create_access_token(
                    data={"sub": form_data.username, "type": "admin"},
                    expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                print(f"Login successful for admin: {form_data.username}")
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_type": "admin"
                }
            print(f"Password verification failed for admin: {form_data.username}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )

# # Route to update user data by username
# @userAuthRouter.put("/update/userdata/{user_name_for_update_data}")
# def update_user_data_by_user_name(user_name_for_update_data: str,
#                                   db: db = Depends(get_db),
#                                   token: str = Depends(oauth2Scheme)):
#     original_user_name = get_user_name_by_token(token)
#     pass
#
#
# # Route to delete user by username
# @userAuthRouter.delete("/delete/{user_name_for_delete_user}")
# def delete_user_by_user_name(user_name_for_delete_user: str):
#     pass
