from datetime import datetime, timedelta
from typing import Optional

from aioify import aioify
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from schemas.secure import User, TokenData
from crud import user as _user
from settings import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


@aioify
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uuid: int = payload.get("sub")
        if uuid is None:
            raise credentials_exception
        token_data = TokenData(uuid=uuid)
    except JWTError:
        raise credentials_exception
    db_user = await _user.get_by_uuid(session, uuid=token_data.uuid)
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
