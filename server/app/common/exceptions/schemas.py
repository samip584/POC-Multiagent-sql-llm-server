from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class ErrorResponseWithMeta(ErrorResponse):
    meta: Any | None
