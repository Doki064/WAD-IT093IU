from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate
import encryption


def create(db: Session, user: UserCreate):
    hashed_password = encryption.hashed_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_by_uid(db: Session, user_uid: int):
<<<<<<< HEAD
    return db.query(User).filter(User.id == user_uid).first()


def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.email == username).first()
=======
    return db.query(User).filter(User.uid == user_uid).first()


def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
>>>>>>> Add CRUD methods


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
<<<<<<< HEAD
=======


def update_password(db: Session, user_uid: int, hashed_password: str):
    db_user = get_by_uid(db, user_uid)
    db_user.hashed_password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user
>>>>>>> Add CRUD methods
