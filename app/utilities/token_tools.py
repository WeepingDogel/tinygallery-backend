from jose import JWTError, jwt
from fastapi import HTTPException, status
from .. import config

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={
        "WWW-Authenticate": "Bearer"
    },
)


# Decode and get username
def get_user_name_by_token(token: str):
    try:
        data_decoder = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=config.ALGORITHM)
        user_name: str = data_decoder.get("sub")
        if user_name is None:
            return False
        return user_name
    except JWTError:
        return False

# Query the database to check if the username exists
