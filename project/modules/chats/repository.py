from uuid import UUID

from sqlalchemy import func, insert, select

from project.core.base_classes.base_repository import BaseRepository
from project.tables.chats import chats
from project.tables.group_participants import group_participant


class ChatRepository(BaseRepository):
    async def create_chat(self, name: str | None, type_: str) -> UUID:
        query = insert(chats).values(name=name, type=type_).returning(chats.c.id)
        return await self.db.fetch_val(query)

    async def add_participants(self, chat_id: UUID, user_ids: list[UUID]) -> None:
        values = [{"chat_id": chat_id, "user_id": uid} for uid in user_ids]
        await self.db.execute_many(query=insert(group_participant), values=values)

    async def get_chat_for_user(self, chat_id: UUID, user_id: UUID) -> dict | None:
        # Подзапрос: проверка, что user_id участвует в чате
        chat_check_subq = (
            select(group_participant.c.chat_id)
            .where((group_participant.c.chat_id == chat_id) & (group_participant.c.user_id == user_id))
            .subquery()
        )

        query = (
            select(
                chats.c.id,
                chats.c.name,
                chats.c.type,
                func.array_agg(group_participant.c.user_id).label("participant_ids"),
            )
            .join(group_participant, group_participant.c.chat_id == chats.c.id)
            .where(chats.c.id.in_(select(chat_check_subq)))
            .group_by(chats.c.id, chats.c.name, chats.c.type)
        )

        row = await self.db.fetch_one(query)
        return dict(row) if row else None

    async def get_chats_for_user(self, user_id: UUID) -> list:
        # 1) Подзапрос: все chat_id, где участвует наш пользователь
        chat_ids_subq = select(group_participant.c.chat_id).where(group_participant.c.user_id == user_id).subquery()

        # 2) Основной запрос:
        #    - джойним всех участников (никаких where по user_id)
        #    - фильтруем чаты по подзапросу
        #    - группируем, собираем array_agg всех user_id
        query = (
            select(
                chats.c.id,
                chats.c.name,
                chats.c.type,
                func.array_agg(group_participant.c.user_id).label("participant_ids"),
            )
            .join(group_participant, group_participant.c.chat_id == chats.c.id)
            .where(chats.c.id.in_(select(chat_ids_subq)))
            .group_by(chats.c.id, chats.c.name, chats.c.type)
        )
        rows = await self.db.fetch_all(query)
        return [dict(row) for row in rows]
