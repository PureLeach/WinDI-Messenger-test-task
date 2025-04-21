import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from project.config.base import settings
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

if __name__ == "__main__":
    pass
