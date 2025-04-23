from datetime import UTC, datetime
from uuid import UUID

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import insert, select, update

from project.core.base_classes.base_repository import BaseRepository
from project.modules.message.models import MessageCreate
from project.tables.group_participants import group_participant
from project.tables.messages import messages


class MessageRepository(BaseRepository):
    async def get_history(self, chat_id: UUID, limit: int = 100, offset: int = 0) -> list[dict]:
        query = (
            select(messages)
            .where(messages.c.chat_id == chat_id)
            .order_by(messages.c.created_at.asc())
            .limit(limit)
            .offset(offset)
        )
        return [dict(row) for row in await self.db.fetch_all(query)]

    async def create_message(self, message: MessageCreate) -> dict | None:
        # We round up to seconds to increase the chances of conflicting identical messages
        created_at = datetime.now(UTC).replace(microsecond=0)
        query = (
            insert(messages)
            .values(
                chat_id=message.chat_id,
                sender_id=message.sender_id,
                text=message.text,
                created_at=created_at,
            )
            .returning(messages)
        )
        try:
            result = await self.db.fetch_one(query)
            return dict(result) if result else None
        except UniqueViolationError:
            # Duplicate handling message if a unique constraint is violated
            return None

    async def update_message_read_status(self, message_id: UUID) -> dict | None:
        query = update(messages).where(messages.c.id == message_id).values(read=True).returning(messages)
        result = await self.db.fetch_one(query)
        return dict(result) if result else None

    async def get_chat_participants(self, chat_id: UUID) -> list[UUID]:
        query = select(group_participant.c.user_id).where(group_participant.c.chat_id == chat_id)
        result = await self.db.fetch_all(query)
        return [row["user_id"] for row in result]
