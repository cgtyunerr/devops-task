"""Airline service."""

from asyncpg import UniqueViolationError
from pydantic import validate_call
from pypika import Query

from app.modules.common import (
    ConflictError,
    create_model_from_query_result,
    NotFoundError,
    Service,
)
from app.modules.airline.models import AirlineBaseModel, AirlineModel
from app.modules.airline.src.service import airline_table


class AirlineService(Service):
    """Airline service class."""

    @validate_call
    async def create_airline(self, body: AirlineBaseModel) -> int:
        """Create airline.

        Arguments:
            body: Airline model.

        Returns:
            The id of the new airline.

        Raises:
            ConflictError: If callsign is conflict.
        """
        query: Query = (
            Query.into(airline_table)
            .columns(
                airline_table.name,
                airline_table.callsign,
                airline_table.founded_year,
                airline_table.base_airport,
            )
            .insert(body.name, body.callsign, body.founded_year, body.base_airport)
        )

        try:
            [[airline_id]] = await self.database.sql.engine.fetch(
                str(query) + " RETURNING id"
            )
            return airline_id
        except UniqueViolationError:
            raise ConflictError("An airline was already created with same callsign.")

    @validate_call
    async def update_airline(self, update_model: AirlineModel) -> None:
        """Update an airline.

        Arguments:
            update_model: An update airline model.
        """
        query = (
            Query.update(airline_table)
            .set(airline_table.name, update_model.name)
            .set(airline_table.callsign, update_model.callsign)
            .set(airline_table.founded_year, update_model.founded_year)
            .set(airline_table.base_airport, update_model.base_airport)
            .where(airline_table.id == update_model.id)
        )

        try:
            await self.execute_in_db(query=query)
        except UniqueViolationError:
            raise ConflictError("An airline was already created with same callsign.")

    @validate_call
    async def get_an_airline(self, airline_id: int) -> AirlineModel:
        """Get an airline with id.

        Arguments:
            airline_id: The airline id.

        Returns
            The airline with the airline_id.

        Raises:
            NotFoundError: The airline with this is not found.
        """
        query = (
            Query.from_(airline_table)
            .select("id", "name", "callsign", "founded_year", "base_airport")
            .where(airline_table.id == airline_id)
        )

        query_result: list[tuple] = await self.fetch_from_db(query=query)

        if not query_result:
            raise NotFoundError("Airline not found.")

        return create_model_from_query_result(
            model=AirlineModel,
            query_result=query_result,
            params=["id", "name", "callsign", "founded_year", "base_airport"],
        )[0]

    @validate_call
    async def get_all_airlines(self) -> list[AirlineModel]:
        """Get all airlines.

        Returns:
            Get all airlines.
        """
        query = Query.from_(airline_table).select(
            "id", "name", "callsign", "founded_year", "base_airport"
        )

        query_result: list[tuple] = await self.fetch_from_db(query=query)

        return create_model_from_query_result(
            model=AirlineModel,
            query_result=query_result,
            params=["id", "name", "callsign", "founded_year", "base_airport"],
        )

    @validate_call
    async def delete_airline(self, airline_id: int) -> None:
        """Delete an airline.

        Arguments:
            airline_id: Airline id.

        Returns:
            None.
        """
        query = (
            Query.from_(airline_table).delete().where(airline_table.id == airline_id)
        )
        await self.execute_in_db(query=query)
