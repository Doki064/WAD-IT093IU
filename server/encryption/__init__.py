import base64
import hashlib
import hmac

import argon2

ph = argon2.PasswordHasher()


def hash_password(password: str) -> str:
    """Hash password function.

    The password is hashed with Argon2,
    after that it is stored in a file to verify in the login process.

    Args:
        password: The password to be hashed.

    Returns:
        Hashed password.
    """
    hashing = base64.b64encode(
        hmac.new(password.encode(), None, hashlib.sha3_256).digest()
    )
    return ph.hash(hashing).encode()


def check_password(hashed_password: str, password: str) -> bool:
    """Check password function, rehash password if needed.

    Argon2 will verify whether the password matches the encrypted key,
    and rehash the password if necessary.

    Args:
        hashed_password: The hashed password stored in the database.
        password: The input password to be checked.

    Returns:
        True if password matches, else False.
    """
    hashing = base64.b64encode(
        hmac.new(password.encode(), None, hashlib.sha3_256).digest()
    )
    try:
        ph.verify(hashed_password, hashing)
    except argon2.exceptions.VerifyMismatchError:
        return False
    return True
