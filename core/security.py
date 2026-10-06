from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 600_000
SALT_LENGTH = 32


def generate_salt() -> bytes:
    """
    Generate a cryptographically secure random salt.
    """

    return secrets.token_bytes(SALT_LENGTH)


def hash_password(password: str) -> str:
    """
    Securely hash a password.

    The returned value contains:
        algorithm
        iterations
        salt
        derived password hash
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    salt = generate_salt()

    password_bytes = password.encode("utf-8")

    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        PASSWORD_ITERATIONS,
    )

    encoded_salt = base64.b64encode(
        salt
    ).decode("ascii")

    encoded_hash = base64.b64encode(
        derived_key
    ).decode("ascii")

    return (
        f"{PASSWORD_ALGORITHM}$"
        f"{PASSWORD_ITERATIONS}$"
        f"{encoded_salt}$"
        f"{encoded_hash}"
    )


def verify_password(
    password: str,
    stored_hash: str,
) -> bool:
    """
    Verify a plain-text password against
    a previously generated password hash.
    """

    if not isinstance(password, str):
        return False

    if not isinstance(stored_hash, str):
        return False

    if not password or not stored_hash:
        return False

    try:
        (
            algorithm,
            iterations_text,
            encoded_salt,
            encoded_hash,
        ) = stored_hash.split("$")

        if algorithm != PASSWORD_ALGORITHM:
            return False

        iterations = int(iterations_text)

        salt = base64.b64decode(
            encoded_salt.encode("ascii")
        )

        expected_hash = base64.b64decode(
            encoded_hash.encode("ascii")
        )

    except (
        ValueError,
        TypeError,
        UnicodeError,
    ):
        return False

    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )

    return hmac.compare_digest(
        calculated_hash,
        expected_hash,
    )


def validate_password_strength(
    password: str,
) -> tuple[bool, str]:
    """
    Validate a password before creating
    a user or changing a password.

    Current minimum policy:
        - at least 8 characters
        - at least one uppercase letter
        - at least one lowercase letter
        - at least one number
    """

    if not isinstance(password, str):
        return False, "Password must be text."

    if len(password) < 8:
        return (
            False,
            "Password must contain at least 8 characters.",
        )

    if not any(
        character.isupper()
        for character in password
    ):
        return (
            False,
            "Password must contain at least one uppercase letter.",
        )

    if not any(
        character.islower()
        for character in password
    ):
        return (
            False,
            "Password must contain at least one lowercase letter.",
        )

    if not any(
        character.isdigit()
        for character in password
    ):
        return (
            False,
            "Password must contain at least one number.",
        )

    return True, "Password meets the minimum security requirements."