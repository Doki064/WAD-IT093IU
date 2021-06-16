import secrets
from typing import List, Union, Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from core import security
from models import User
from schemas.internal import UserCreate


async def create(db: Session, user: UserCreate) -> User:
    salt = secrets.token_bytes(16)
    encoded_password = security.secret_password(user.password, salt)
    db_user = User(
        username=user.username,
        hashed_password=encoded_password,
        salt=salt.hex(),
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    await db.commit()
    return db_user


async def get_by_id(db: Session, user_id: int) -> Union[User, None]:
    q = select(User).where(User.id == user_id)
    result = await db.execute(q)
    return result.scalars().first()


async def get_by_uuid(db: Session, uuid: UUID) -> Union[User, None]:
    q = select(User).where(User.uuid == uuid)
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
    if not security.verify_password(db_user.hashed_password, password, salt):
        return None
    return db_user


async def rehash_password(db: Session, user_id: int, password: str):
    salt = secrets.token_bytes(16)
    hashed_password = security.hash_password(password, salt)
    q = update(User).where(User.id == user_id)
    q.values(hashed_password=hashed_password)
    q.values(salt=salt.hex())
    await db.execute(q)
    await db.commit()
