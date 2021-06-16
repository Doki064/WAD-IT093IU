from typing import Optional
from datetime import datetime, timedelta
from uuid import UUID

from aioify import aioify
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from schemas.internal import User, TokenPayload
from crud import user as _user
from database.config import async_session
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PATH}/users/login/auth")


@aioify
def sign_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authorize_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        uuid: UUID = payload.get("sub")
        if uuid is None:
            raise credentials_exception
        token_data = TokenPayload(sub=uuid)
    except JWTError:
        raise credentials_exception

    async with async_session() as session:
        async with session.begin():
            db_user = await _user.get_by_uuid(session, uuid=token_data.sub)
            if db_user is None:
                raise credentials_exception
            return db_user


async def get_current_active_user(current_user: User = Depends(authorize_token)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: User = Depends(authorize_token)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
