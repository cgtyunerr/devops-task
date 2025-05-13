"""Unit tests for utils."""

import pytest

from app.modules.common import AuthenticationError
from app.modules.user.src.service.utils import check_password


class TestCheckPassword:
    def test_wrong_password(self):
        with pytest.raises(AuthenticationError) as error:
            check_password(
                "test1234",
                "$2b$12$nM9GDZntSdILRqAfU58UweoPHwcVfESldlhp84Ms1nFwVkYaXv9aO",
            )

        assert str(error.value) == "Login credentials are not correct."

    def test_success(self):
        check_password(
            "testtest",
            "$2b$12$nM9GDZntSdILRqAfU58UweoPHwcVfESldlhp84Ms1nFwVkYkXv9aO",
        )
