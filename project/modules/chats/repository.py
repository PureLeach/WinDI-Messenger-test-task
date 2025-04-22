from uuid import UUID, uuid4

from sqlalchemy import insert

from project.core.base_classes.base_repository import BaseRepository
from project.tables.chats import chats
from project.tables.group_participants import group_participant


class ChatRepository(BaseRepository):
    async def create_chat(self, name: str | None, type_: str) -> UUID:
        query = insert(chats).values(id=uuid4(), name=name, type=type_).returning(chats.c.id)
        return await self.db.fetch_val(query)

    async def add_participants(self, chat_id: UUID, user_ids: list[UUID]) -> None:
        values = [{"chat_id": chat_id, "user_id": uid} for uid in user_ids]
        await self.db.execute_many(query=insert(group_participant), values=values)
