from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utilities.hash_tool import verify_password
from app import config
from app.model import crud

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
    :param token: Token to get UserName.
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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
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
def authenticate_user(db: Session, username: str, password: str):
    try:
        user = crud.get_user_by_name(db=db, user_name=username)
        if not user:
            print(f"User authentication failed: User '{username}' not found")
            return False
        
        print(f"Found user: {username}")
        print(f"Stored hash: {user.password}")
        
        is_valid = verify_password(password, user.password)
        print(f"Password validation result for {username}: {is_valid}")
        
        return user if is_valid else False
        
    except Exception as e:
        print(f"Authentication error for user {username}: {str(e)}")
        return False

def authenticate_admin(db: Session, username: str, password: str):
    try:
        admin = crud.get_admin_by_name(db=db, user_name=username)
        if not admin:
            print(f"Admin authentication failed: Admin '{username}' not found")
            return False
            
        print(f"Found admin: {username}")
        print(f"Stored hash: {admin.password}")
        
        is_valid = verify_password(password, admin.password)
        print(f"Password validation result for admin {username}: {is_valid}")
        
        return admin if is_valid else False
        
    except Exception as e:
        print(f"Authentication error for admin {username}: {str(e)}")
        return False
