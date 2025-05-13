"""Airline pydantic models."""

from pydantic import BaseModel


class AirlineBaseModel(BaseModel):
    """Airline model.

    Arguments:
        name: Name of airline.
        callsign: Callsign of airline.
        founded_year: Foundation year of airline.
        base_airport: Base of airline.
    """

    name: str
    callsign: str
    founded_year: str
    base_airport: str


class AirlineModel(AirlineBaseModel):
    """Airline model.

    Arguments:
        id: The airline id.
    """

    id: int
