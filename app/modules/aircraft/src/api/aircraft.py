"""Router for aircraft module."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette import status

from app.api.dependencies import get_current_user
from app.modules.aircraft.models import AircraftModel, AircraftBaseModel
from app.modules.aircraft.src.factory import AircraftFactory
from app.modules.aircraft.src.service.aircraft import AircraftService


aircraft_router = APIRouter(
    prefix="/aircraft",
    tags=["aircraft"],
)

aircraft_factory = AircraftFactory()
aircraft_service: AircraftService = aircraft_factory()


class AircraftIdPathDependency(BaseModel):
    """Aircraft ID path dependency."""

    aircraft_id: int = Path(
        description="The aircraft ID.",
    )


@aircraft_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=int,
    summary="Create new aircraft.",
)
async def create_aircraft(
    body: AircraftBaseModel,
    user_id: Annotated[int, Depends(get_current_user)],
):
    """Create new aircraft."""
    result = await aircraft_service.create_aircraft(body=body)
    return ORJSONResponse(content=jsonable_encoder(result))


@aircraft_router.patch(
    path="/{aircraft_id}/",
    summary="Update aircraft.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_aircraft(
    user_id: Annotated[int, Depends(get_current_user)],
    body: AircraftBaseModel,
    aircraft_id: Annotated[AircraftIdPathDependency, Depends()],
):
    """Update aircraft."""
    await aircraft_service.update_aircraft(
        update_model=AircraftModel(
            id=aircraft_id.aircraft_id,
            manufacturer_serial_number=body.manufacturer_serial_number,
            type=body.type,
            model=body.model,
            operator_airline=body.operator_airline,
            number_of_engines=body.number_of_engines,
        )
    )


@aircraft_router.get(
    path="/{aircraft_id}/",
    summary="Get an airline.",
    status_code=status.HTTP_200_OK,
    response_model=AircraftModel,
)
async def get_an_aircraft(
    user_id: Annotated[int, Depends(get_current_user)],
    aircraft_id: Annotated[AircraftIdPathDependency, Depends()],
):
    """Get an aircraft."""
    result = await aircraft_service.get_an_aircraft(aircraft_id=aircraft_id.aircraft_id)
    return ORJSONResponse(content=jsonable_encoder(result))


@aircraft_router.delete(
    path="/{aircraft_id}/",
    summary="Delete airline.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_aircraft(
    user_id: Annotated[int, Depends(get_current_user)],
    aircraft_id: Annotated[AircraftIdPathDependency, Depends()],
):
    """Delete aircraft."""
    await aircraft_service.delete_aircraft(aircraft_id=aircraft_id.aircraft_id)
