"""Unit tests for user service."""

import pytest

from tests import database

from app.modules.common import ConflictError

from app.modules.common import AuthenticationError
from app.modules.user.models import UserCreateModel
from app.modules.user.src.service.user import UserService


@pytest.fixture
def user_service() -> UserService:
    """User service fixture."""
    return UserService(database=database)


class TestGetUserFromDB:
    async def test_success(self, user_service):
        (
            user_id,
            username,
            hashed_pw,
        ) = await user_service._get_user_from_db(username="deneme")
        assert isinstance(user_id, int)
        assert isinstance(username, str)
        assert isinstance(hashed_pw, str)

        assert user_id == 1
        assert (
            hashed_pw == "$2b$12$nM9GDZntSdILRqAfU58UweoPHwcVfESldlhp84Ms1nFwVkYkXv9aO"
        )

    async def test_error_with_nonexistent_username(self, user_service):
        with pytest.raises(AuthenticationError) as error:
            await user_service._get_user_from_db("not_existing_username")

        assert str(error.value) == "Login credentials are not correct."


class TestInsertToDB:
    async def test_error(self, user_service):
        with pytest.raises(ConflictError) as error:
            await user_service._insert_user_to_db(
                body=UserCreateModel(
                    username="deneme",
                    password="test@sensgreen.com",
                ),
                hashed_pw="hashedpassword",
            )
        assert str(error.value) == "Username is already in use."

    async def test_success(self, user_service):
        try:
            user_id = await user_service._insert_user_to_db(
                body=UserCreateModel(
                    username="deneme8",
                    password="test@newuser.com",
                ),
                hashed_pw="hashedstrongpassword",
            )

            assert isinstance(user_id, int)

            [(new_user_id, user_name, password)] = await database.sql.engine.fetch(
                "SELECT id,username,password FROM "
                "users.user WHERE username='deneme8'"
            )

            assert new_user_id == user_id
            assert user_name == "deneme8"
            assert password == "hashedstrongpassword"

        finally:
            await database.sql.engine.execute(
                "DELETE FROM users.user WHERE username='deneme8'"
            )
