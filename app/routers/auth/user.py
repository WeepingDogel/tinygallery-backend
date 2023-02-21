from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ...model import schemas
from ...model import crud
from ...db import get_db
from ... import config

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


def verifyPassword(plain_password, hashed_password):
    return pwdContext.verify(plain_password, hashed_password)


def getPasswordHash(password):
    return pwdContext.hash(password)


def CreateAccessToken(data: dict, expires_delta: timedelta | None = None):
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

def AuthenticateUser(db: Session, userName: str, password: str):
    user = crud.GetUserByName(db, userName=userName)
    if not user:
        return False
    if not verifyPassword(password, user.password):
        return False
    return True

@userAuthRouter.post("/register")
async def CreateUser(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.GetUserByName(db, userName=user.userName)
    if user.userName == "" or user.password == "" or user.email == "":
        raise HTTPException(
            status_code=400, detail="Username, password and email can't be empty.")
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username has already existed!")
    user.password = getPasswordHash(user.password)
    crud.CreateUser(db=db, user=user)
    return {"status": "success"}

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@userAuthRouter.post("/token")
async def userLogin(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    UserAuthentication = AuthenticateUser(db, form_data.username, form_data.password)
    if not UserAuthentication:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    AccessTokenExpires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    AccessToken = CreateAccessToken(
        data={"sub":form_data.username},
        expires_delta=AccessTokenExpires)
    return {"access_token": AccessToken, "token_type":"bearer"}


@userAuthRouter.get("/test")
async def TokenTest(token: str = Depends(oauth2Scheme)):
    return {"status":token}