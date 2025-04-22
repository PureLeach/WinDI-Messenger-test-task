import uuid

from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from project.config.db import metadata

chats = Table(
    "chats",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=True),
    Column("type", String, nullable=False),  # 'private' or 'group'
)
