"""Unit test for airline service."""

import pytest

from tests import database

from app.modules.airline.models import AirlineModel, AirlineBaseModel
from app.modules.airline.src.service.airline import AirlineService


@pytest.fixture
def airline_service() -> AirlineService:
    """Create and return airline service instance."""
    return AirlineService(database=database)


class TestCreateAirline:
    async def test_add_airline(self, airline_service):
        try:
            result = await airline_service.create_airline(
                body=AirlineBaseModel(
                    name="British Airlines",
                    callsign="BA",
                    founded_year="1954",
                    base_airport="Gatwick",
                )
            )

            assert isinstance(result, int)

            [(airline_id, name, callsign, founded_year, base_airport)] = (
                await database.sql.engine.fetch(
                    "select id, name, callsign, founded_year, base_airport "
                    "from airlines.airline "
                    f"where id = {result}"
                )
            )

            assert airline_id == result
            assert name == "British Airlines"
            assert callsign == "BA"
            assert founded_year == "1954"
            assert base_airport == "Gatwick"

        finally:
            await database.sql.engine.execute(
                "delete from airlines.airline " "where callsign = 'BA'"
            )

    async def test_conflict_error(self, airline_service):
        with pytest.raises(ValueError) as error:
            await airline_service.create_airline(
                body=AirlineBaseModel(
                    name="British Airlines",
                    callsign="THY",
                    founded_year="1954",
                    base_airport="Gatwick",
                )
            )
        assert str(error.value) == "An airline was already created with same callsign."


class TestUpdateAirline:
    async def test_update_airline(self, airline_service):
        try:
            await airline_service.update_airline(
                update_model=AirlineModel(
                    id=1,
                    name="Turkish airlines",
                    callsign="THYAO",
                    founded_year="1984",
                    base_airport="IST",
                )
            )

            [(airline_id, name, callsign, founded_year, base_airport)] = (
                await database.sql.engine.fetch(
                    "select id, name, callsign, founded_year, base_airport "
                    "from airlines.airline "
                    "where id = 1"
                )
            )

            assert airline_id == 1
            assert name == "Turkish airlines"
            assert callsign == "THYAO"
            assert founded_year == "1984"
            assert base_airport == "IST"

        finally:
            await database.sql.engine.execute(
                "UPDATE airlines.airline SET callsign = 'THY' WHERE id = 1"
            )

    async def test_update_error(self, airline_service):
        with pytest.raises(ValueError) as error:
            await airline_service.update_airline(
                update_model=AirlineModel(
                    id=1,
                    name="Turkish airlines",
                    callsign="QA",
                    founded_year="1984",
                    base_airport="IST",
                )
            )
        assert str(error.value) == "An airline was already created with same callsign."


class TestGetAirline:
    async def test_get_an_airline(self, airline_service):
        result: AirlineModel = await airline_service.get_an_airline(airline_id=1)
        assert result.id == 1
        assert result.name == "Turkish airlines"
        assert result.callsign == "THY"
        assert result.founded_year == "1984"
        assert result.base_airport == "IST"

    async def test_error_get_an_airline(self, airline_service):
        with pytest.raises(ValueError) as error:
            await airline_service.get_an_airline(airline_id=3)

        assert str(error.value) == "Airline not found."

    async def test_get_all_airlines(self, airline_service):
        result: list[AirlineModel] = await airline_service.get_all_airlines()
        assert len(result) == 2


class TestDeleteAirline:
    async def test_delete_airline(self, airline_service):
        await database.sql.engine.execute(
            "INSERT INTO airlines.airline "
            "(id, name, callsign, founded_year, base_airport) "
            "VALUES "
            "(3, 'deneme', 'ss', '1877', 'LON')"
        )
        result: list[AirlineModel] = await airline_service.get_all_airlines()
        assert len(result) == 3

        await airline_service.delete_airline(airline_id=3)
        result: list[AirlineModel] = await airline_service.get_all_airlines()
        assert len(result) == 2
