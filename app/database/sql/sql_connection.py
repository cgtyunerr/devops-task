"""Module to store SQL engine."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from aiocache import cached
from asyncpg import create_pool
from asyncpg.pool import Pool
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from .sql_operations import SqlOperations


class SqlEngine(BaseModel):
    """PSQL engine class.

    Attributes:
        name: Name of the database.
        user: User of the database.
        password: Password of the database.
        host: Host of the database.
        port: Port of the database.

    Methods:
        fetch: Fetch the result of the query.
        execute: Execute the query.
        __call__: Create a context manager for transaction.
    """

    host: str = Field("localhost", validate_default=True)
    name: str = Field("postgres", validate_default=True)
    password: str = Field("dbpass", validate_default=True)
    user: str = Field("dbuser", validate_default=True)
    port: int = Field(5432, validate_default=True)

    N_ATTEMPS: int = 3
    WAIT_MULTIPLIER: float = 0.1

    @cached()
    async def _get_pool(self) -> Pool:
        """Get database connection pool."""
        return await create_pool(
            **{
                "user": self.user,
                "password": self.password,
                "host": self.host,
                "port": str(self.port),
                "database": self.name,
            },
            min_size=5,
            max_size=20,
            command_timeout=90,
        )

    @retry(
        stop=stop_after_attempt(N_ATTEMPS),
        wait=wait_exponential(multiplier=WAIT_MULTIPLIER),
        reraise=True,
    )
    async def fetch(self, query: str, *args) -> list[tuple]:
        """Return the result of executing the passed query.

        Arguments:
            query: Query to perform.
            args: Variables to replace.

        Returns:
            The result of executing the passed query.
        """
        pool: Pool = await self._get_pool()
        query_result: list
        async with pool.acquire() as conn:
            connection: SqlOperations = SqlOperations(connection=conn)
            query_result = await connection.fetch(query, *args)
        return query_result

    @retry(
        stop=stop_after_attempt(N_ATTEMPS),
        wait=wait_exponential(multiplier=WAIT_MULTIPLIER),
        reraise=True,
    )
    async def execute(self, query: str) -> None:
        """Execute the passed query.

        Arguments:
            query: Query to perform.
        """
        pool: Pool = await self._get_pool()
        async with pool.acquire() as conn:
            connection: SqlOperations = SqlOperations(connection=conn)
            await connection.execute(query)

    @asynccontextmanager
    async def __call__(self) -> AsyncIterator:
        """Create a context manager for transaction."""
        pool: Pool = await self._get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                yield SqlOperations(connection=conn)
