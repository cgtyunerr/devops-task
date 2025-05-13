"""Aircraft service factory."""

from functools import lru_cache

from app import database
from app.modules.aircraft.src.service.aircraft import AircraftService


class AircraftFactory:
    """Aircraft factory class."""

    @staticmethod
    @lru_cache(maxsize=1)
    def __call__() -> AircraftService:
        """Return the class instance based on the class name."""
        return AircraftService(database=database)
