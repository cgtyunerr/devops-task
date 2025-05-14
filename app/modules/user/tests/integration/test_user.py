"""Integration tests for user service."""

from unittest.mock import ANY, patch

from jose import jwt

from tests import (
    mock_async_func_returning_id,
    mock_func_returning_id,
)

from app.config import settings
from app.modules.user.models import UserCreateModel

from app.modules.user.src.service.user import UserService
from app.modules.user.tests.unit.test_user import user_service

_ = user_service


class TestLogin:
    @patch(
        "app.modules.user.src.service.user.check_password",
        side_effect=mock_func_returning_id,
    )
    async def test_success(self, mock_check_password, user_service):
        async def get_user(*args, **kwargs):
            return 100, "deneme5", "hashed_pw"

        with patch.object(
            UserService, "_get_user_from_db", side_effect=get_user
        ) as mock_get:
            result = await user_service.login(
                username="deneme5", password="testpassword"
            )

            mock_get.assert_called_once_with(username="deneme5")

            mock_check_password.assert_called_once_with(
                password="testpassword", hashed_pw="hashed_pw"
            )

            decoded_token = jwt.decode(result.access_token, settings.JWT_SECRET)

            assert len(decoded_token) == 1
            assert decoded_token["user_id"] == 100


class TestRegister:

    @patch.object(
        UserService,
        "_insert_user_to_db",
        side_effect=mock_async_func_returning_id,
    )
    async def test_success(self, mock_insert, user_service):
        body: UserCreateModel = UserCreateModel(
            username="deneme5",
            password="testpassword",
        )
        assert await user_service.register(body=body)

        mock_insert.assert_called_once_with(body=body, hashed_pw=ANY)
