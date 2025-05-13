"""Aircraft service."""

from asyncpg import UniqueViolationError
from pydantic import validate_call
from pypika import Query

from app.modules.common import (
    ConflictError,
    create_model_from_query_result,
    NotFoundError,
    Service,
)
from app.modules.aircraft.models import AircraftModel, AircraftBaseModel
from app.modules.aircraft.src.service import aircraft_table


class AircraftService(Service):
    """Airline service class."""

    @validate_call
    async def create_aircraft(self, body: AircraftBaseModel) -> int:
        """Create aircraft.

        Arguments:
            body: AircraftBaseModel.

        Returns:
            The id of the new aircraft.

        Raises:
            ConflictError: If manufacturer serial number is conflict.
        """
        query: Query = (
            Query.into(aircraft_table)
            .columns(
                aircraft_table.manufacturer_serial_number,
                aircraft_table.type,
                aircraft_table.model,
                aircraft_table.operator_airline,
                aircraft_table.number_of_engines,
            )
            .insert(
                body.manufacturer_serial_number,
                body.type,
                body.model,
                body.operator_airline,
                body.number_of_engines,
            )
        )

        try:
            [[aircraft_id]] = await self.database.sql.engine.fetch(
                str(query) + " RETURNING id"
            )
            return aircraft_id
        except UniqueViolationError:
            raise ConflictError(
                "An aircraft was already created with same manufacturer serial number."
            )

    @validate_call
    async def update_aircraft(self, update_model: AircraftModel) -> None:
        """Update an aircraft.

        Arguments:
            update_model: An update aircraft model.
        """
        query = (
            Query.update(aircraft_table)
            .set(
                aircraft_table.manufacturer_serial_number,
                update_model.manufacturer_serial_number,
            )
            .set(aircraft_table.type, update_model.type)
            .set(aircraft_table.model, update_model.model)
            .set(aircraft_table.operator_airline, update_model.operator_airline)
            .set(aircraft_table.number_of_engines, update_model.number_of_engines)
            .where(aircraft_table.id == update_model.id)
        )

        try:
            await self.execute_in_db(query=query)
        except UniqueViolationError:
            raise ConflictError(
                "An aircraft was already created with same manufacturer serial number."
            )

    @validate_call
    async def get_an_aircraft(self, aircraft_id: int) -> AircraftModel:
        """Get an aircraft with id.

        Arguments:
            aircraft_id: The aircraft id.

        Returns
            The aircraft with the aircraft_id.

        Raises:
            NotFoundError: The aircraft with this is not found.
        """
        query = (
            Query.from_(aircraft_table)
            .select(
                "id",
                "manufacturer_serial_number",
                "type",
                "model",
                "operator_airline",
                "number_of_engines",
            )
            .where(aircraft_table.id == aircraft_id)
        )

        query_result: list[tuple] = await self.fetch_from_db(query=query)

        if not query_result:
            raise NotFoundError("Aircraft not found.")

        return create_model_from_query_result(
            model=AircraftModel,
            query_result=query_result,
            params=[
                "id",
                "manufacturer_serial_number",
                "type",
                "model",
                "operator_airline",
                "number_of_engines",
            ],
        )[0]

    @validate_call
    async def delete_aircraft(self, aircraft_id: int) -> None:
        """Delete an aircraft.

        Arguments:
            aircraft_id: Aircraft id.

        Returns:
            None.
        """
        query = (
            Query.from_(aircraft_table).delete().where(aircraft_table.id == aircraft_id)
        )
        await self.execute_in_db(query=query)
