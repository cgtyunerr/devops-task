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


class UserLogin(BaseModel):
    """User login model.

    Attributes:
        access_token: Access token.
        token_type: Token type (bearer).
        username: Email of the user.
    """

    access_token: str
    token_type: str
    username: str
