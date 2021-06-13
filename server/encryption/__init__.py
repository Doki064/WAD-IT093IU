import base64
import hashlib
import hmac
import os
from pathlib import Path

from dotenv import load_dotenv
from passlib.context import CryptContext

BASE_DIR = Path(__file__).absolute().parents[1]
load_dotenv(BASE_DIR.joinpath(".env"))

pwd_context = CryptContext(
    schemes=os.environ["HASH_METHOD"],
    deprecated="auto",
)


def hash_password(password: str, salt: bytes) -> str:
    """Hash password function.

    The password is hashed with Argon2,
    after that it is stored in a file to verify in the login process.

    Args:
        password: The password to be hashed.
        salt: The salt to strengthen hash.

    Returns:
        Hashed password.
    """
    secret = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest())
    return pwd_context.hash(secret)


def check_password(password: str, hashed_password: str, salt: bytes):
    """Check password function, rehash password if needed.

    Argon2 will verify whether the password matches the encrypted key,
    and rehash the password if necessary.

    Args:
        password: The input password to be checked.
        hashed_password: The hashed password stored in the database.
        salt: The salt stored in the database.

    Returns:
        True if password matches, else False.

    Raises:
        NeedRehashException: Exception raised when password needs to be rehashed.
    """
    secret = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest())
    return pwd_context.verify(secret, hashed_password)


def needs_rehash(hashed_password: str):
    return pwd_context.needs_update(hashed_password)
