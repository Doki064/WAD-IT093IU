import base64
import hashlib
import hmac

import argon2

ph = argon2.PasswordHasher()


class NeedRehashException(Exception):
    pass


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
    signature = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest())
    return ph.hash(signature).encode()


def check_password(hashed_password: str, password: str, salt: bytes) -> bool:
    """Check password function, rehash password if needed.

    Argon2 will verify whether the password matches the encrypted key,
    and rehash the password if necessary.

    Args:
        hashed_password: The hashed password stored in the database.
        password: The input password to be checked.
        salt: The salt stored in the database.

    Returns:
        True if password matches, else False.

    Raises:
        NeedRehashException: Exception raised when password needs to be rehashed.
    """
    signature = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest())
    try:
        ph.verify(hashed_password, signature)
        if ph.check_needs_rehash(hashed_password):
            raise NeedRehashException
    except argon2.exceptions.VerifyMismatchError:
        return False
    return True
