"""Airline service factory."""

from functools import lru_cache

from app import database
from app.modules.airline.src.service.airline import AirlineService


class AirlineFactory:
    """Airline factory class."""

    @staticmethod
    @lru_cache(maxsize=1)
    def __call__() -> AirlineService:
        """Return the class instance based on the class name."""
        return AirlineService(database=database)
