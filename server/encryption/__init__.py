import base64
import hashlib
import hmac

import argon2

ph = argon2.PasswordHasher()


def hash_password(encryption_file: str, password):
    """Hash password function.

    The password is hashed with Argon2,
    after that it is stored in a file to verify in the login process.

    Args:
        encryption_file: Path to the file storing the encrypted security key.
        password: The password for the app, which will be hashed, defaults to "python".

    Returns:
        str: Hashed password.
    """
    hashing = base64.b64encode(
        hmac.new(password.encode(), None, hashlib.sha3_256).digest()
    )
    # with open(encryption_file, "w+b") as f:
    # f.write(ph.hash(hashing).encode())
    return ph.hash(hashing).encode()


def check_password(encryption_file: str, password: str) -> bool:
    """Check password function, rehash password if needed.

    Argon2 will verify whether the password matches the encrypted key,
    and rehash the password if necessary.

    Args:
        encryption_file: Path to the file storing the encrypted security key.
        password: The password to check with the encryption key.

    Returns:
        True if password matches, else False.
    """
    hashing = base64.b64encode(
        hmac.new(password.encode(), None, hashlib.sha3_256).digest()
    )
    try:
        with open(encryption_file, "r+b") as f:
            hashed = f.read().decode()
            ph.verify(hashed, hashing)
            if ph.check_needs_rehash(hashed):
                f.write(ph.hash(hashing).encode())

    except argon2.exceptions.VerifyMismatchError:
        return False
    return True
