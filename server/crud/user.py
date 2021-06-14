from typing import List, Union, Optional
import secrets

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import encryption
from models import User


async def create(db: Session, username: str, password: str) -> User:
    salt = secrets.token_bytes(16)
    hashed_password = encryption.hash_password(password, salt)
    db_user = User(username=username, hashed_password=hashed_password, salt=salt.hex())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_by_uid(db: Session, user_uid: int) -> Union[User, None]:
    q = select(User).where(User.uid == user_uid)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_username(db: Session, username: str) -> Union[User, None]:
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


async def authenticate(session, username: str, password: str):
    db_user = await get_by_username(session, username=username)
    if db_user is None:
        return None
    salt = bytes.fromhex(db_user.salt)
    if not encryption.verify_password(db_user.hashed_password, password, salt):
        return None
    if encryption.needs_rehash(db_user.hashed_password):
        await rehash_password(session, user_uid=db_user.uid, password=password)
    return db_user


async def rehash_password(db: Session, user_uid: int, password: str):
    salt = secrets.token_bytes(16)
    hashed_password = encryption.hash_password(password, salt)
    q = update(User).where(User.uid == user_uid)
    q.values(hashed_password=hashed_password)
    q.values(salt=salt.hex())
    await db.execute(q)
    await db.commit()
