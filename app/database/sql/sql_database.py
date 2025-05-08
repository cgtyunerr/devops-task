"""Sql database module."""

from pydantic import BaseModel

from .sql_connection import SqlEngine


class SqlDatabase(BaseModel):
    """Sql Database class.

    Attributes:
        engine: PSqlEngine to use for performing the database operations.
    """

    engine: SqlEngine
