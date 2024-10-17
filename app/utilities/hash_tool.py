from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwdContext.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwdContext.verify(plain_password, hashed_password)  # Use passlib's verify method
