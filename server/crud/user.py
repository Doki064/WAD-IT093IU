from typing import List, Optional
import secrets

# from jose import JWTError, jwt
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import encryption
from models import User
from schemas import UserCreate


async def create(db: Session, user: UserCreate) -> User:
    salt = secrets.token_bytes(16)
    hashed_password = encryption.hash_password(user.password, salt)
    db_user = User(username=user.username,
                   hashed_password=hashed_password,
                   salt=salt.hex())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_by_uid(db: Session, user_uid: int) -> User:
    q = select(User).where(User.uid == user_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_username(db: Session, username: str) -> User:
    q = select(User).where(User.username == username)
    result = await db.execute(q)
    return result.scalars().first()


async def get_all(db: Session,
                  skip: Optional[int] = None,
                  limit: Optional[int] = None) -> List[User]:
    q = select(User)
    if skip is not None:
        q.offset(skip)
    if limit is not None:
        q.limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


async def rehash_password(db: Session, user_uid: int, password: str):
    salt = secrets.token_bytes(16)
    hashed_password = encryption.hash_password(password, salt)
    q = update(User).where(User.uid == user_uid)
    q.values(hashed_password=hashed_password)
    q.values(salt=salt.hex())
    await db.execute(q)
    await db.commit()
