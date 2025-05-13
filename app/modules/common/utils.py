"""Shared utils functions."""

from logging import Logger
from typing import Type, TypeVar

from pydantic import BaseModel, validate_call

from app.modules.common.logger import get_logger


T = TypeVar("T", bound=BaseModel)

logger: Logger = get_logger()


@validate_call
def create_model_from_query_result(
    model: Type[T],
    query_result: list[tuple],
    params: list[str],
) -> list[T]:
    """Create a model by using the query result.

    Arguments:
        model: The base model class.
        query_result: Query result.
        params: Query's parameters. (order is important.)

    Returns:
        List of the model instances.
    """
    return [model(**dict(zip(params, row))) for row in query_result]
