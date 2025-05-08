"""Database class."""

from .factory import DatabaseFactory
from .sql import SqlDatabase


class Database:
    """Database class.

    Attributes:
        sql: SQL Database instance.
    """

    def __init__(self):
        """Create a database instance."""
        self.sql: SqlDatabase = DatabaseFactory.get_sql_database_instance()
