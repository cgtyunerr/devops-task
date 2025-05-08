"""Shared service class."""

from logging import Logger

from pydantic import BaseModel, ConfigDict, validate_call

from pypika.queries import QueryBuilder

from app.database import Database
from .logger import get_logger


class Service(BaseModel):
    """Service class.

    The database instances are shared between its methods.

    Attributes:
        database: Database instance.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    database: Database
    logger: Logger = get_logger()

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    async def fetch_from_db(self, query: QueryBuilder) -> list[tuple]:
        """Fetch data from the database.

        Arguments:
            query: The query to execute.

        Returns:
            The fetched data.
        """
        return await self.database.sql.engine.fetch(str(query))

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    async def execute_in_db(self, query: QueryBuilder) -> None:
        """Execute a query in the database.

        Arguments:
            query: The query to execute.
        """
        await self.database.sql.engine.execute(str(query))
