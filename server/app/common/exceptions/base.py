from fastapi import FastAPI

from app.common.exceptions import common_exceptions
from app.common.exceptions import db_exceptions
from app.common.exceptions import generic_exceptions


def add_exception_handlers(app: FastAPI) -> None:
    """
    Add different exception handlers for common, generic and db specific exceptions
    """
    db_exc = db_exceptions.DatabaseException
    db_exc_handler = db_exceptions.database_error_handler

    common_exc = common_exceptions.CommonException
    common_exc_handler = common_exceptions.common_error_handler

    generic_exc_handler = generic_exceptions.generic_error_handler

    app.add_exception_handler(db_exc, db_exc_handler)
    app.add_exception_handler(common_exc, common_exc_handler)
    app.add_exception_handler(Exception, generic_exc_handler)
