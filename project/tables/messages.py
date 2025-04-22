import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from project.config.db import metadata

messages = Table(
    "messages",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("uuid", UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),
    Column("chat_id", UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False),
    Column("sender_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("text", String, nullable=False),
    Column("timestamp", DateTime, default=datetime.utcnow),
    Column("read", Boolean, default=False),
)
