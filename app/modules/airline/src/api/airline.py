"""Router for airline module."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette import status

from app.api.dependencies import get_current_user
from app.modules.airline.models import AirlineBaseModel, AirlineModel
from app.modules.airline.src.factory import AirlineFactory
from app.modules.airline.src.service.airline import AirlineService


airline_router = APIRouter(
    prefix="/airline",
    tags=["airline"],
)

airline_factory = AirlineFactory()
airline_service: AirlineService = airline_factory()


class AirlineIdPathDependency(BaseModel):
    """Airline ID path dependency."""

    airline_id: int = Path(
        description="The airline ID.",
    )


@airline_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=int,
    summary="Create new airline.",
)
async def create_airline(
    body: AirlineBaseModel,
    user_id: Annotated[int, Depends(get_current_user)],
):
    """Create new airline."""
    result = await airline_service.create_airline(body=body)
    return ORJSONResponse(content=jsonable_encoder(result))


@airline_router.patch(
    path="/{airline_id}/",
    summary="Update airline.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_airline(
    user_id: Annotated[int, Depends(get_current_user)],
    body: AirlineBaseModel,
    airline_id: Annotated[AirlineIdPathDependency, Depends()],
):
    """Update airline."""
    await airline_service.update_airline(
        update_model=AirlineModel(
            id=airline_id.airline_id,
            name=body.name,
            callsign=body.callsign,
            founded_year=body.founded_year,
            base_airport=body.base_airport,
        )
    )


@airline_router.get(
    path="/{airline_id}/",
    summary="Get an airline.",
    status_code=status.HTTP_200_OK,
    response_model=AirlineModel,
)
async def get_an_airline(
    user_id: Annotated[int, Depends(get_current_user)],
    airline_id: Annotated[AirlineIdPathDependency, Depends()],
):
    """Get an airline."""
    result = await airline_service.get_an_airline(airline_id=airline_id.airline_id)
    return ORJSONResponse(content=jsonable_encoder(result))


@airline_router.get(
    path="/",
    summary="Get all airlines.",
    status_code=status.HTTP_200_OK,
    response_model=list[AirlineModel],
)
async def get_all_airlines(
    user_id: Annotated[int, Depends(get_current_user)],
):
    """Get all airlines."""
    result = await airline_service.get_all_airlines()
    return ORJSONResponse(content=jsonable_encoder(result))


@airline_router.delete(
    path="/{airline_id}/",
    summary="Delete airline.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_airline(
    user_id: Annotated[int, Depends(get_current_user)],
    airline_id: Annotated[AirlineIdPathDependency, Depends()],
):
    """Delete airline."""
    await airline_service.delete_airline(airline_id=airline_id.airline_id)
