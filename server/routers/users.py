"""All user route methods."""
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

import encryption
from database.config import async_session
from schemas.secure import User, Token, TokenData
from crud import user as _user
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {
        "description": "Not found"
    }},
)


async def _get_current_user(session, token: str = Depends(encryption.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uid: int = payload.get("sub")
        if user_uid is None:
            raise credentials_exception
        token_data = TokenData(user_uid=user_uid)
    except JWTError:
        raise credentials_exception
    db_user = await _user.get_by_uid(session, user_uid=token_data.user_uid)
    if db_user is None:
        raise credentials_exception
    return db_user


async def _get_current_active_user(current_user: User = Depends(_get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.authenticate(session, form_data.username,
                                               form_data.password)
            if db_user is None:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            access_token = encryption.create_access_token(
                data={"sub": f"user_uid:{db_user.user_uid}"},
                expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/", response_model=Token, status_code=201)
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_username(session, username=form_data.username)
            if db_user is not None:
                raise HTTPException(status_code=409, detail="Username already exists")
            db_user = await _user.create(session,
                                         username=form_data.username,
                                         password=form_data.password)
            access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            access_token = encryption.create_access_token(
                data={"sub": f"user_uid:{db_user.user_uid}"},
                expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=User)
async def read_user_me(current_user: User = Depends(_get_current_active_user)):
    return current_user


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
