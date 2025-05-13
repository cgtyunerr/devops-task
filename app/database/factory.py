"""Database factory."""

from app.config import settings
from .sql import SqlDatabase
from .sql.sql_connection import SqlEngine


class DatabaseFactory:
    """Database factory class."""

    _sql_database_instance: SqlDatabase = None

    @classmethod
    def get_sql_database_instance(cls) -> SqlDatabase:
        """Get the SQL database instance.

        If the instance does not exist, create it.
        (Check singleton pattern)

        Returns:
            The SQL database instance.
        """
        if cls._sql_database_instance is None:
            cls._sql_database_instance = SqlDatabase(
                engine=SqlEngine(
                    host=settings.DB.HOST,
                    name=settings.DB.NAME,
                    password=settings.DB.PASS,
                    user=settings.DB.USER,
                    port=settings.DB.PORT,
                )
            )

        return cls._sql_database_instance
