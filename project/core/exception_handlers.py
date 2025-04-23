from typing import Any

from asyncpg.exceptions import PostgresError, UniqueViolationError
from fastapi.responses import JSONResponse
from starlette.requests import Request

from project.config.base import settings

logger = settings.LOGGER.getChild(__name__)


async def unique_violation_handler(_: Request, exc: Any) -> JSONResponse:
    logger.error(f"Unique violation error: {exc}")
    if isinstance(exc, UniqueViolationError):
        detail = str(exc).split("DETAIL:")[-1].strip() if "DETAIL:" in str(exc) else "Unique constraint violated"
        return JSONResponse(status_code=409, content={"error": "Conflict", "detail": detail})
    return JSONResponse(status_code=409, content={"error": "Conflict", "detail": "Unique violation"})


async def postgres_error_handler(_: Request, exc: Any) -> JSONResponse:
    logger.error(f"Postgres error: {exc}")
    if isinstance(exc, PostgresError):
        return JSONResponse(status_code=400, content={"error": "Database error", "detail": str(exc)})
    return JSONResponse(status_code=400, content={"error": "Database error"})
