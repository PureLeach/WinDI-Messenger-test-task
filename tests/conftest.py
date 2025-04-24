import asyncio
import pathlib
from collections.abc import AsyncGenerator

import pytest
from alembic import command, config
from httpx import ASGITransport, AsyncClient
from sqlalchemy_utils import create_database, database_exists, drop_database

from project.config.base import settings
from project.config.db import metadata
from project.main import app

pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.chats",
    "tests.fixtures.group_participants",
    "tests.fixtures.messages",
]


@pytest.fixture(scope="function", autouse=True)
def anyio_backend():
    return "asyncio", {"use_uvloop": True}


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()


@pytest.fixture(scope="session")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
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


@pytest.fixture(scope="function")
async def db():
    async with settings.DB.db_instance as db:
        yield db


@pytest.fixture(autouse=True, scope="function")
async def clean_db(db):
    transaction = await db.transaction()
    try:
        # await db.execute(text("SET session_replication_role = 'replica';"))
        for table in reversed(metadata.sorted_tables):
            await db.execute(table.delete())
            # await db.execute(text("SET session_replication_role = 'origin';"))
    except Exception:
        await transaction.rollback()
    else:
        await transaction.commit()
