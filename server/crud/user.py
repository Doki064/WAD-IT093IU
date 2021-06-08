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
    return db.query(User).filter(User.id == user_uid).first()


def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.email == username).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
