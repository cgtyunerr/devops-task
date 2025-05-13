"""User factory module."""

from functools import lru_cache

from app import database
from app.modules.user.src.service.user import UserService


class UserFactory:
    """User factory class."""

    @staticmethod
    @lru_cache(maxsize=1)
    def __call__() -> UserService:
        """Return the class instance based on the class name."""
        return UserService(database=database)
