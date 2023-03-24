from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from ...utilities.image_tools import generate_default_avatar
from ...utilities.userdata_tool import get_user_uuid_by_name
from ...model import schemas
from ...model import crud
from app.dependencies.db import get_db
from ... import config
from ...dependencies.oauth2scheme import oauth2Scheme
from ...utilities.token_tools import get_user_name_by_token

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
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwdContext.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwdContext.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, userName: str, password: str):
    user = crud.get_user_by_name(db, user_name=userName)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return True


@userAuthRouter.post("/register")
# User Registration
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=user.user_name)
    # Information check
    if user.user_name == "" or user.password == "" or user.email == "":
        raise HTTPException(
            status_code=400, detail="Username, password and email can't be empty.")
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username has already existed!")
    # Password encrypt
    user.password = get_password_hash(user.password)
    crud.create_user(db=db, user=user)
    # Give out the default avatar.
    generate_default_avatar(user_uuid=get_user_uuid_by_name(user_name=user.user_name, db=db))
    return {"status": "success"}


@userAuthRouter.post("/token")
async def user_login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_authentication = authenticate_user(
        db, form_data.username, form_data.password)

    if not user_authentication:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=access_token_expires)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot create token.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"access_token": access_token, "token_type": "bearer"}


@userAuthRouter.put("/update/userdata/{user_name_for_update_data}")
def update_user_data_by_user_name(user_name_for_update_data: str,
                                  db: Session = Depends(get_db),
                                  token: str = Depends(oauth2Scheme)):
    original_user_name = get_user_name_by_token(token)
    pass


@userAuthRouter.delete("/delete/{user_name_for_delete_user}")
def delete_user_by_user_name(user_name_for_delete_user: str):
    pass
