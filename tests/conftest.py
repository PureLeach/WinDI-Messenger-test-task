import asyncio
import pathlib
from collections.abc import AsyncGenerator

import pytest
from alembic import command, config
from httpx import ASGITransport, AsyncClient
from sqlalchemy_utils import create_database, database_exists, drop_database

from project.config.base import settings
from project.main import app


@pytest.fixture(scope="function", autouse=True)
def anyio_backend():
    return "asyncio", {"use_uvloop": True}


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest.fixture(scope="session")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://krakend") as async_client:
        yield async_client


@pytest.fixture(scope="session", autouse=True)
async def create_test_db() -> AsyncGenerator[None, None]:
    sync_url = settings.DB.DATABASE_DSN.replace("asyncpg", "psycopg2")
    try:
        if not database_exists(sync_url):
            create_database(sync_url)
        # Setup alembic and apply migrations:
        config_path = pathlib.Path(__file__).parent.parent / "project/alembic.ini"
        alembic_config = config.Config(str(config_path))
        command.upgrade(alembic_config, "head")
        yield
    finally:
        drop_database(sync_url)


# Method 1. It works, but the transaction rollback does not occur
@pytest.fixture(scope="function")
async def db():
    async with settings.DB.db_instance as db:
        yield db


# Method 2. First test pass, but program freezes when executing `await transaction.rollback()`
# @pytest.fixture(scope="function")
# async def db():
#     async with settings.DB.db_instance as db:
#         transaction = db.transaction(isolation='serializable')
#         await transaction.start()
#         yield db
#         await transaction.rollback()


# Method 3. First test pass, but program raises exception IndexError: list index out of range
# @pytest.fixture(scope="function")
# async def db():
#     db = settings.DB.db_instance
#     await db.connect()
#     transaction = await db.transaction()
#     try:
#         yield db
#     finally:
#         await transaction.rollback()
#         await db.disconnect()


# Method 4. databases/core.py:473: AssertionError
# @pytest.fixture(scope="function")
# async def db():
#     async with Database(settings.DB.DATABASE_DSN, force_rollback=True) as db:
#         yield db
