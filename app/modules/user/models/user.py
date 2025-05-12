"""User pydantic models."""

from pydantic import BaseModel


class UserCreateModel(BaseModel):
    """User create model.

    Attributes:
        username: str
        password: str
    """

    username: str
    password: str
