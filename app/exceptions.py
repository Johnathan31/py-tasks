from logging import getLogger
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg import Error

logger = getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(Error)
    async def handle_database_error(
        _: Request,
        exc: Error
    ) -> JSONResponse:
        logger.exception("Database error occurred.", exc_info=exc)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Database Error"
            }
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        _: Request,
        exc: Exception
    ) -> JSONResponse:
        logger.exception("Unexpected server error.", exc_info=exc)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error"
            }
        )

    @app.exception_handler(HTTPException)
    def handle_http_exceptions(
        _: Request,
        exc: HTTPException
    ):
        logger.exception("HTTP Exception occurred:", exc_info=exc)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.detail
            }
        )

    @app.exception_handler(RequestValidationError)
    def handle_request_validation_error(
        _: Request,
        exc: RequestValidationError
    ):
        logger.exception(
            "Validation error occured on the request", exc_info=exc)

        return JSONResponse(
            status_code=422,
            content={
                "error": "Request Validation Error",
                "details": exc.errors()
            }
        )
