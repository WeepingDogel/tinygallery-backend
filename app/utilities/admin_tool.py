from .hash_tool import get_password_hash
from .json_config_reader import read_admin_list
from app.model.crud import create_admin, get_admin_by_name
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.dependencies.db import engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import ADMIN_LIST

get_db = sessionmaker(bind=engine)


def create_admin_users(db: Session = get_db(), admin_list: list = read_admin_list(ADMIN_LIST)):
    if not admin_list:
        raise ValueError("Admin list is empty")
    num_created = 0
    for admin in admin_list:
        if not get_admin_by_name(user_name=admin['username'], db=db):
            try:
                create_admin(user=admin, db=db, password_hashed=get_password_hash(admin['password']))
            except SQLAlchemyError:
                print("SQLAlchemy Error!")
                return False
            except OperationalError:
                print("[Error] User has already existed:" + admin['username'])
            finally:
                print("[OK] Admin created successfully:" + admin['username'])
    if num_created > 0:
        return True
    else:
        return False
