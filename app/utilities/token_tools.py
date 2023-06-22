from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .hash_tool import verify_password
from .. import config
from ..model import crud

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={
        "WWW-Authenticate": "Bearer"
    },
)


# Decode and get username
# Query the database to check if the username exists
def get_user_name_by_token(token: str):
    """
    :param token:
    :return a username:
    """
    try:
        data_decoder = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=config.ALGORITHM)
        user_name: str = data_decoder.get("sub")
        if user_name is None:
            return False
        return user_name
    except JWTError:
        return False


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


# Function to authenticate user
def authenticate_user(db: Session, userName: str, password: str):
    user = crud.get_user_by_name(db=db, user_name=userName)
    if not user:
        return False
    elif not verify_password(password, user.password):
        return False
    return True


def authenticate_admin(db: Session, userName: str, password: str):
    admin = crud.get_admin_by_name(db=db, user_name=userName)
    if not admin:
        return False
    elif not verify_password(password, admin.password):
        return False
    return True
