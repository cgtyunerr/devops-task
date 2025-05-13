"""Unit test for aircraft service."""

import pytest

from tests import database

from app.modules.aircraft.models import AircraftModel, AircraftBaseModel
from app.modules.aircraft.src.service.aircraft import AircraftService


@pytest.fixture
def aircraft_service() -> AircraftService:
    """Create and return airline service instance."""
    return AircraftService(database=database)


class TestCreateAirline:
    async def test_add_airline(self, aircraft_service):
        try:
            result = await aircraft_service.create_aircraft(
                body=AircraftBaseModel(
                    manufacturer_serial_number="4631",
                    type="Airbus",
                    model="Airbus A319-132",
                    operator_airline="2",
                    number_of_engines=5,
                )
            )

            assert isinstance(result, int)

            [
                (
                    aircraft_id,
                    manufacturer_serial_number,
                    aircraft_type,
                    model,
                    operator_airline,
                    number_of_engines,
                )
            ] = await database.sql.engine.fetch(
                "select id, manufacturer_serial_number, type, "
                "model, operator_airline, number_of_engines "
                "from aircrafts.aircraft "
                f"where id = {result}"
            )

            assert aircraft_id == result
            assert manufacturer_serial_number == "4631"
            assert aircraft_type == "Airbus"
            assert model == "Airbus A319-132"
            assert operator_airline == "2"
            assert number_of_engines == 5

        finally:
            await database.sql.engine.execute(
                "delete from aircrafts.aircraft "
                "where manufacturer_serial_number = '4631'"
            )

    async def test_conflict_error(self, aircraft_service):
        with pytest.raises(ValueError) as error:
            await aircraft_service.create_aircraft(
                body=AircraftBaseModel(
                    manufacturer_serial_number="4629",
                    type="Airbus",
                    model="Airbus A319-132",
                    operator_airline="2",
                    number_of_engines=5,
                )
            )
        assert (
            str(error.value)
            == "An aircraft was already created with same manufacturer serial number."
        )


class TestUpdateAirline:
    async def test_update_airline(self, aircraft_service):
        try:
            await aircraft_service.update_aircraft(
                update_model=AircraftModel(
                    id=1,
                    manufacturer_serial_number="4631",
                    type="Airbus",
                    model="Airbus A319-132",
                    operator_airline="1",
                    number_of_engines=5,
                )
            )

            [
                (
                    aircraft_id,
                    manufacturer_serial_number,
                    aircraft_type,
                    model,
                    operator_airline,
                    number_of_engines,
                )
            ] = await database.sql.engine.fetch(
                "select id, manufacturer_serial_number, type, model, "
                "operator_airline, number_of_engines "
                "from aircrafts.aircraft "
                "where id = 1"
            )

            assert aircraft_id == 1
            assert manufacturer_serial_number == "4631"
            assert aircraft_type == "Airbus"
            assert model == "Airbus A319-132"
            assert operator_airline == "1"
            assert number_of_engines == 5

        finally:
            await database.sql.engine.execute(
                "UPDATE aircrafts.aircraft SET manufacturer_serial_number = '4629' "
                "WHERE id = 1"
            )

    async def test_update_error(self, aircraft_service):
        with pytest.raises(ValueError) as error:
            await aircraft_service.update_aircraft(
                update_model=AircraftModel(
                    id=1,
                    manufacturer_serial_number="4630",
                    type="Airbus",
                    model="Airbus A319-132",
                    operator_airline="2",
                    number_of_engines=5,
                )
            )
        assert (
            str(error.value)
            == "An aircraft was already created with same manufacturer serial number."
        )


class TestGetAirline:
    async def test_get_an_aircraft(self, aircraft_service):
        result: AircraftModel = await aircraft_service.get_an_aircraft(aircraft_id=1)
        assert result.id == 1
        assert result.manufacturer_serial_number == "4629"
        assert result.type == "Airbus"
        assert result.model == "Airbus A319-132"
        assert result.operator_airline == "1"
        assert result.number_of_engines == 5

    async def test_error_get_an_aircraft(self, aircraft_service):
        with pytest.raises(ValueError) as error:
            await aircraft_service.get_an_aircraft(aircraft_id=3)

        assert str(error.value) == "Aircraft not found."


class TestDeleteAirline:
    async def test_delete_aircraft(self, aircraft_service):
        await database.sql.engine.execute(
            "INSERT INTO aircrafts.aircraft "
            "(id, manufacturer_serial_number, type, "
            "model, operator_airline, number_of_engines) "
            "VALUES "
            "(3, 'deneme', 'ss', '1877 Leon', '4', 12)"
        )
        result: AircraftModel = await aircraft_service.get_an_aircraft(aircraft_id=3)
        assert result.id == 3

        await aircraft_service.delete_aircraft(aircraft_id=3)
        with pytest.raises(ValueError) as error:
            await aircraft_service.get_an_aircraft(aircraft_id=3)

        assert str(error.value) == "Aircraft not found."
