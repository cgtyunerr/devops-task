"""User service utils."""

from functools import lru_cache

from passlib.context import CryptContext
from pydantic import validate_call

from app.modules.common import AuthenticationError


@lru_cache(maxsize=1)
def get_password_context() -> CryptContext:
    """Get password context."""
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


@validate_call
def hash_password(password: str) -> str:
    """Hash the password.

    Arguments:
        password: The password to hash.

    Returns:
        The hashed password.
    """
    return get_password_context().hash(password)


@validate_call
def check_password(password: str, hashed_pw: str) -> None:
    """Check the password with the hashed one.

    Arguments:
        password: Password to check.
        hashed_pw: Hashed password to compare.

    Returns:
        None.

    Raises:
        LoginFailedError: If the password is not correct.
    """
    if not get_password_context().verify(password, hashed_pw):
        raise AuthenticationError("Login credentials are not correct.")
