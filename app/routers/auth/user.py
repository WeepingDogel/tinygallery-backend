from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from ...model import schemas
from ...model import crud
from ...db import get_db
from ... import config
from ...dependencies.oauth2scheme import oauth2Scheme

userAuthRouter = APIRouter(
    prefix="/auth",
    tags=['Auth'],
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
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user_name=user.user_name)

    if user.user_name == "" or user.password == "" or user.email == "":
        raise HTTPException(
            status_code=400, detail="Username, password and email can't be empty.")
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username has already existed!")

    user.password = get_password_hash(user.password)
    crud.create_user(db=db, user=user)
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

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@userAuthRouter.get("/test")
async def token_test(token: str = Depends(oauth2Scheme)):
    return {"status": token}
