"""All user route methods."""
from fastapi import APIRouter, HTTPException

import encryption
from database.config import async_session
from schemas import User, UserCreate
from crud import user as _user

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.post("/login/", response_model=User)
async def login(user: UserCreate):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_username(session, username=user.username)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            salt = bytes.fromhex(db_user.salt)
            if not encryption.check_password(db_user.hashed_password, user.password,
                                             salt):
                raise HTTPException(status_code=401, detail="Login failed")
            if encryption.needs_rehash(db_user.hashed_password):
                await _user.rehash_password(session,
                                            user_uid=db_user.uid,
                                            password=user.password)
            return db_user


@router.post("/register/", response_model=User, status_code=201)
async def register(user: UserCreate):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_username(session, username=user.username)
            if db_user is not None:
                raise HTTPException(status_code=409, detail="Username already exists")
            return await _user.create(session, user=user)


@router.get("/", response_model=User)
async def read_users(username: str):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_username(session, username=username)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user


@router.get("/{user_uid}", response_model=User)
async def read_user(user_uid: int):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_uid(session, user_uid=user_uid)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user
