from uuid import UUID

from project.modules.chats.exception import ChatFoundError
from project.modules.chats.models import ChatCreate, ChatOut
from project.modules.chats.repository import ChatRepository


class ChatService:
    def __init__(self, repository: ChatRepository) -> None:
        self.repository = repository

    async def create_chat(self, chat_data: ChatCreate) -> ChatOut:
        async with self.repository.db.transaction():
            chat_id = await self.repository.create_chat(chat_data.name, chat_data.type)
            await self.repository.add_participants(chat_id, chat_data.participant_ids)
            return ChatOut(
                id=chat_id,
                name=chat_data.name,
                type=chat_data.type,
                participant_ids=chat_data.participant_ids,
            )

    async def add_user_to_chat(self, chat_id: UUID, user_id: UUID) -> ChatOut:
        async with self.repository.db.transaction():
            await self.repository.add_participants(chat_id, [user_id])
            chat = await self.repository.get_chat_for_user(chat_id, user_id)
            if chat is None:
                raise ChatFoundError(message="Chat not found")
            return ChatOut(**chat)

    async def get_chats_for_user(self, user_id: UUID) -> list[ChatOut]:
        chats = await self.repository.get_chats_for_user(user_id)
        result: list[ChatOut] = []
        for chat in chats:
            chat["participant_ids"] = list(chat["participant_ids"])
            result.append(ChatOut(**chat))
        return result
