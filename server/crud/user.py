from sqlalchemy.orm import Session

import models
import schemas
import encryption


def create(db: Session, user: schemas.UserCreate):
    hashed_password = encryption.hashed_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get(db: Session, user_uid: int):
    return db.query(models.User).filter(models.User.id == user_uid).first()


def get_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.email == username).first()


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
