"""App module."""

from datetime import datetime, timezone

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.modules import ErrorHandlerMiddleware
from app.modules.airline import airline_router
from app.modules.aircraft import aircraft_router
from app.modules.user import user_router

app: FastAPI = FastAPI(
    title="Airline rest api.",
    description="Airline Rest Api project.",
    version="1.0.8",
)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandlerMiddleware)

app.include_router(user_router)
app.include_router(airline_router)
app.include_router(aircraft_router)


@app.get(
    "/health/",
    response_model=dict[str, str | datetime],
    summary="Get Health Information.",
)
async def check_health():
    """Check Health Condition of The System."""
    result: dict[str, str | datetime] = {
        "message": "OK",
        "timestamp": datetime.now(timezone.utc),
    }

    return ORJSONResponse(
        content=jsonable_encoder(result), status_code=status.HTTP_200_OK
    )
