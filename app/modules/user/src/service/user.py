"""User service."""

from asyncpg import UniqueViolationError
from jose import jwt
from pydantic import validate_call
from pypika import Query

from app.config import settings
from app.modules.common import ConflictError, Service, AuthenticationError
from app.modules.user.models import UserCreateModel, UserLogin
from app.modules.user.src.service import user_table
from app.modules.user.src.service.utils import check_password, hash_password


class UserService(Service):
    """User service class."""

    @validate_call
    async def login(self, username: str, password: str) -> UserLogin:
        """Login the user.

        Arguments:
            username: Username of the user.
            password: Password of the user.

        Returns:
            Bearer token.

        Raises:
            AuthenticationError: If login failed for any reason, we just raise one
                error for not revealing information.
        """
        user_id: int
        hashed_pw: str
        partner_id: int
        user_id, _, hashed_pw = await self._get_user_from_db(username=username)

        check_password(password=password, hashed_pw=hashed_pw)

        token: str = jwt.encode({"user_id": user_id}, settings.JWT_SECRET)
        login_result: UserLogin = UserLogin(
            username=username,
            access_token=token,
            token_type="bearer",
        )

        return login_result

    @validate_call
    async def register(self, body: UserCreateModel) -> int:
        """Register a new user.

        Arguments:
            body: User create model.

        Returns:
            int: Created users ID.

        Raises:
            ConflictError: If Email is already registered.
        """
        # Hash the password and insert the user to the database.
        hashed_pw: str = hash_password(password=body.password)
        user_id: int = await self._insert_user_to_db(body=body, hashed_pw=hashed_pw)

        return user_id

    # Helpers.
    @validate_call
    async def _get_user_from_db(self, username: str) -> tuple[int, str, str]:
        """Get user from the database by filtering either email or user_id.

        Arguments:
            username: Username of the user to filter.

        Returns:
            Tuple of user id, username, hashed password.

        Raises:
            AuthenticationError: If no user found with the given identifier.
        """
        hashed_pw: str
        query = (
            Query.from_(user_table)
            .select(
                user_table.id,
                user_table.username,
                user_table.password,
            )
            .where(user_table.username == username)
        )

        try:
            [(user_id, username, hashed_pw)] = await self.fetch_from_db(query)
            return user_id, username, hashed_pw
        except ValueError:
            raise AuthenticationError("Login credentials are not correct.")

    @validate_call
    async def _insert_user_to_db(self, body: UserCreateModel, hashed_pw: str) -> int:
        """Insert user to the database.

         Arguments:
            body: User create model.
            hashed_pw: Hashed password of the user.

        Returns:
            Created user's ID.

        Raises:
            ConflictError: If username is already registered.
        """
        query: Query = (
            Query.into(user_table)
            .columns(
                user_table.username,
                user_table.password,
            )
            .insert(body.username, hashed_pw)
        )

        try:
            # Using fetch for returning the id of the created user.
            [[user_id]] = await self.database.sql.engine.fetch(
                str(query) + " RETURNING id"
            )
            return user_id
        except UniqueViolationError:
            raise ConflictError("Username is already in use.")
