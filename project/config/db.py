from urllib.parse import quote

from databases import Database
from pydantic import PostgresDsn, PrivateAttr, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

from project.core.helpers.db import connection_init

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


class DBConfig(BaseSettings):
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB_NAME: str = ""

    DATABASE_DSN: str = ""
    _database: Database | None = PrivateAttr(None)

    @field_validator("DATABASE_DSN", mode="before")
    @classmethod
    def assemble_db_dsn(cls, _: str, values: ValidationInfo) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.data["POSTGRES_USER"],
                password=quote(values.data["POSTGRES_PASSWORD"]),
                host=values.data["POSTGRES_HOST"],
                port=values.data["POSTGRES_PORT"],
                path=f'{values.data["POSTGRES_DB_NAME"]}',
            ),
        )

    @property
    def db_instance(self) -> Database:
        if self._database is None:
            create_async_engine(self.DATABASE_DSN, echo=True)
            self._database = Database(self.DATABASE_DSN, server_settings={"jit": "off"}, init=connection_init)
        return self._database
