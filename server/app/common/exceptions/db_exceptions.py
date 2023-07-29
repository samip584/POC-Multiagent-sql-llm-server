from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from .schemas import ErrorResponse


class DatabaseException(Exception):
    def __init__(self, *args: object) -> None:  # pylint: disable=useless-parent-delegation
        super().__init__(*args)


def database_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Global error handler for database exceptions.
    """
    headers = getattr(exc, "headers", None)

    if isinstance(exc, (DatabaseException)):
        error = ErrorResponse(detail="Database Error")

        if headers:
            return JSONResponse(
                content=error.model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                headers=headers,
            )

        return JSONResponse(
            content=error.model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(
        content=ErrorResponse(detail="Internal Server Error").model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
