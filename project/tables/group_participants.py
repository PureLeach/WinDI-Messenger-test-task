from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from project.config.db import metadata

group_participant = Table(
    "group_participants",
    metadata,
    Column("chat_id", UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)
