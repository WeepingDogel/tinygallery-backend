from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwdContext.hash(password)


def verify_password(plain_password, hashed_password):
    return pwdContext.verify(plain_password, hashed_password)
