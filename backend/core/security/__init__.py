import base64
import hashlib
import hmac

from sqlalchemy_utils import Password


def secret_password(password: str, salt: bytes) -> Password:
    """Encoded password function.

    An encoded secret string is generated from password and salt,
        after that it will be hashed to store in the database.

    Args:
        password: The password to be hashed.
        salt: The salt to strengthen hash.

    Returns:
        A password object.
    """
    secret = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest()
    )
    return Password(value=secret, secret=True)


def verify_password(hashed_password: Password, password: str, salt: bytes) -> bool:
    """Verify password function, rehash password if needed.

    Verify whether password matches the hash in the database.

    Args:
        password: The input password to be checked.
        hashed_password: The hashed password stored in the database.
        salt: The salt stored in the database.

    Returns:
        True if password matches, False otherwise.
    """
    secret = base64.b64encode(
        hmac.new(password.encode(), salt, hashlib.sha3_256).digest()
    )
    return hashed_password == secret
