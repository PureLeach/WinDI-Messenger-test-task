from project.modules.chats.models import ChatCreate, ChatOut
from project.modules.chats.repository import ChatRepository


class ChatService:
    def __init__(self, repository: ChatRepository) -> None:
        self.repository = repository

    async def create_chat(self, chat_data: ChatCreate) -> ChatOut:
        async with self.repository.db.transaction():
            chat_id = await self.repository.create_chat(chat_data.name, chat_data.type)
            await self.repository.add_participants(chat_id, chat_data.participant_ids)
            return ChatOut(id=chat_id, name=chat_data.name, type=chat_data.type, participant_ids=chat_data.participant_ids)
