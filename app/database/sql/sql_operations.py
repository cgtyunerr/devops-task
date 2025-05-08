"""Sql operations class."""

from asyncpg.connection import Connection
from pydantic import BaseModel, ConfigDict, validate_call


class SqlOperations(BaseModel):
    """Sql operations class."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    connection: Connection

    @validate_call()
    async def fetch(self, query: str, *args) -> list[tuple]:
        """Database fetch operation.

        Arguments:
            query: Query to perform.
            args: Variables to replace.

        Return:
            Result of executing query as a list of tuple.
        """
        return [tuple(row) for row in await self.connection.fetch(query, *args)]

    @validate_call()
    async def execute(self, query: str) -> None:
        """Database execute operation.

        Arguments:
            query: Query to perform.

        Return:
            None.
        """
        await self.connection.execute(query)
