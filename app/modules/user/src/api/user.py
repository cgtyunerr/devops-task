"""Router for user module."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.modules.user.models import UserCreateModel, UserLogin
from app.modules.user.src.factory import UserFactory
from app.modules.user.src.service.user import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)

# Service instance.
user_factory = UserFactory()
user_service: UserService = user_factory()


@user_router.post(
    "/register/",
    response_model=int,
    summary="Register new user.",
    status_code=status.HTTP_201_CREATED,
)
async def register(body: UserCreateModel):
    """Register a new user."""
    result: int = await user_service.register(body)

    return ORJSONResponse(content=jsonable_encoder(result))


@user_router.post(
    "/login/",
    summary="Allows the user to login.",
    response_model=UserLogin,
    status_code=status.HTTP_201_CREATED,
)
async def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login the user."""
    result = await user_service.login(
        username=form_data.username,
        password=form_data.password,
    )

    return ORJSONResponse(content=jsonable_encoder(result))
