import base64
import hashlib
import hmac
import os
# from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

# BASE_DIR = Path(__file__).absolute().parents[1]
# load_dotenv(BASE_DIR.joinpath(".env"))

HASH_SCHEME = os.environ["HASH_SCHEME"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(
    schemes=HASH_SCHEME,
    deprecated="auto",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str, salt: bytes) -> str:
    """Hash password function.

    Hash is generate from password and salt, after that it will be stored in the database.

    Args:
        password: The password to be hashed.
        salt: The salt to strengthen hash.

    Returns:
        Hashed password.
    """
    secret = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest())
    return pwd_context.hash(secret)


def verify_password(password: str, hashed_password: str, salt: bytes):
    """Verify password function, rehash password if needed.

    Verify whether password matches the hash in the database.

    Args:
        password: The input password to be checked.
        hashed_password: The hashed password stored in the database.
        salt: The salt stored in the database.

    Returns:
        True if password matches, False otherwise.

    Raises:
        NeedRehashException: Exception raised when password needs to be rehashed.
    """
    secret = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest())
    return pwd_context.verify(secret, hashed_password)


def needs_rehash(hashed_password: str):
    """Check if old hashed password needs to be rehashed.

    Args:
        hashed_password: The hashed password stored in the database.

    Returns:
        True if needs to be rehashed, False otherwise.
    """
    return pwd_context.needs_update(hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
