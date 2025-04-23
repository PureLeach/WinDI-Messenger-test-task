from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, func, text
from sqlalchemy.dialects.postgresql import UUID

from project.config.db import metadata

messages = Table(
    "messages",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("chat_id", UUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False),
    Column("sender_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", DateTime(timezone=True), index=False, nullable=False, server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        index=True,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    Column("read", Boolean, nullable=False, server_default="false"),
)
