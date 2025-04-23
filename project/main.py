import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from asyncpg.exceptions import PostgresError, UniqueViolationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.config.base import settings
from project.core.exception_handlers import postgres_error_handler, unique_violation_handler
from project.core.routers import register_routers


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    await settings.DB.db_instance.connect()
    yield
    await settings.DB.db_instance.disconnect()


def setup_logging_context() -> None:
    logging.basicConfig(
        level=settings.LOGGING.LEVEL,
        format=settings.LOGGING.FORMAT,
        datefmt=settings.LOGGING.DATE_FORMAT,
    )


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    dependencies=[],
    lifespan=lifespan,
)
setup_logging_context()
register_routers(app)

app.add_exception_handler(UniqueViolationError, unique_violation_handler)
app.add_exception_handler(PostgresError, postgres_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    pass
