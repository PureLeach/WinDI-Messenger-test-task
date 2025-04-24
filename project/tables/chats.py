from sqlalchemy import Column, Enum, String, Table, text
from sqlalchemy.dialects.postgresql import UUID

from project.config.db import metadata
from project.modules.chats.models import ChatType

chats = Table(
    "chats",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("name", String, nullable=True),
    Column("type", Enum(ChatType), nullable=False),
)
