from fastapi.security import OAuth2PasswordBearer

# For authentication
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/user/token")