from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from .schemas import ErrorResponse


class GenericException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def generic_error_handler(_: Request, exc: GenericException) -> JSONResponse:
    """
    Generic error handler for the application.
    """
    headers = getattr(exc, "headers", None)

    if headers:
        error = ErrorResponse(detail="An error occurred while processing your request")
        return JSONResponse(
            content=error.model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=headers,
        )

    error = ErrorResponse(detail="Internal Server Error")
    return JSONResponse(
        content=error.model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
