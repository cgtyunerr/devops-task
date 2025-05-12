"""Common exceptions."""


class InvalidInputError(ValueError):
    """Invalid input."""


class NotFoundError(ValueError):
    """Not found."""


class ConflictError(ValueError):
    """Item conflict."""


class UnprocessableEntityError(ValueError):
    """Item is unprocessable."""
