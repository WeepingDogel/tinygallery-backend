from passlib.context import CryptContext
import logging

# 创建一个全局的CryptContext实例
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # 设置哈希轮数
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        print("-" * 50)
        print("Password Verification Debug:")
        print(f"Plain password (len={len(plain_password)}): {plain_password}")
        print(f"Stored hash (len={len(hashed_password)}): {hashed_password}")
        
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"Verification result: {result}")
        print("-" * 50)
        return result
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    try:
        hashed = pwd_context.hash(password)
        print("-" * 50)
        print("Password Hashing Debug:")
        print(f"Original password (len={len(password)}): {password}")
        print(f"Generated hash (len={len(hashed)}): {hashed}")
        print("-" * 50)
        return hashed
    except Exception as e:
        print(f"Password hashing error: {str(e)}")
        raise e
