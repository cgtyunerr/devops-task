"""Shared dependencies for HTTP API."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from app.config import settings


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/user/login/")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """Get the current user id from the token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET)
        return payload["user_id"]

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
