from sqlalchemy import Column, String, Table, text
from sqlalchemy.dialects.postgresql import UUID

from project.config.db import metadata

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)
