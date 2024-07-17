import logging
from typing import Any

from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from .schemas import ErrorResponse
from .schemas import ErrorResponseWithMeta

logger = logging.getLogger(__name__)


class CommonException(HTTPException):
    """
    Base internal server error exception.
    """

    meta = None

    def __init__(
        self, detail: Any, meta: Any, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs
    ) -> None:
        if meta is not None:
            self.meta = meta
        super().__init__(detail=detail, status_code=status_code, **kwargs)


class UnauthorizedException(CommonException):
    """
    Unauthorized exception.
    """

    def __init__(
        self, detail="Unauthorized", status_code: int = status.HTTP_401_UNAUTHORIZED, meta=None, **kwargs
    ) -> None:
        super().__init__(detail=detail, status_code=status_code, meta=meta, **kwargs)


class BadRequest(CommonException):
    """
    HTTP Exception for client side errors.
    """

    def __init__(self, detail="Bad request", meta=None, **kwargs) -> None:
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST, meta=meta, **kwargs)


class NotFound(CommonException):
    """
    HTTP Exception for resource not found errors.
    """

    def __init__(self, detail="Resource not found", meta=None, **kwargs) -> None:
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND, meta=meta, **kwargs)


def common_error_handler(_: Request, exc: CommonException) -> JSONResponse:
    """
    Global error handler for common HTTP Exceptions
    """
    error = ErrorResponse(detail=exc.detail)

    if exc.meta is not None:
        error = ErrorResponseWithMeta(detail=exc.detail, meta=exc.meta)

    headers = getattr(exc, "headers", None)

    logger.error(error)

    if isinstance(exc, CommonException):
        if headers:
            return JSONResponse(
                content=error.model_dump(),
                status_code=exc.status_code,
                headers=headers,
            )

        return JSONResponse(
            content=error.model_dump(),
            status_code=exc.status_code,
        )

    return JSONResponse(
        content=ErrorResponse(detail="Internal Server Error").model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
