import secrets

from sqlalchemy.orm import Session

import encryption
from models import User
from schemas import UserCreate


def create(db: Session, user: UserCreate):
    salt = secrets.token_bytes(16)
    hashed_password = encryption.hash_password(user.password, salt)
    db_user = User(username=user.username,
                   hashed_password=hashed_password,
                   salt=salt.hex())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_by_uid(db: Session, user_uid: int):
    return db.query(User).filter(User.uid == user_uid).first()


def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_password(db: Session, user_uid: int, hashed_password: str):
    db_user = get_by_uid(db, user_uid)
    db_user.hashed_password = hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user
