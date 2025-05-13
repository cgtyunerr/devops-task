"""Aircraft pydantic models."""

from pydantic import BaseModel


class AircraftBaseModel(BaseModel):
    """Airline model.

    Arguments:
        manufacturer_serial_number: Manufacturer unique serial number..
        type: Type of aircraft.
        model: Model of aircraft.
        operator_airline: Base of airline.
        number_of_engines: Number of engines.
    """

    manufacturer_serial_number: str
    type: str
    model: str
    operator_airline: str
    number_of_engines: int


class AircraftModel(AircraftBaseModel):
    """Airline model.

    Arguments:
        id: The airline id.
    """

    id: int
