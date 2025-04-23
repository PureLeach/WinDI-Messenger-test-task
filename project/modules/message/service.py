from uuid import UUID

from project.modules.message.exception import MessageFoundError
from project.modules.message.models import MessageCreate, MessageOut
from project.modules.message.repository import MessageRepository


class MessageService:
    def __init__(self, repository: MessageRepository) -> None:
        self.repository = repository

    async def get_history(self, chat_id: UUID, limit: int = 100, offset: int = 0) -> list[MessageOut]:
        history = await self.repository.get_history(chat_id, limit, offset)
        return [MessageOut(**message) for message in history]

    async def validate_connection(self, chat_id: UUID, user_id: UUID) -> bool:
        chat_participants = await self._get_chat_participants(chat_id)
        return user_id in chat_participants

    async def _get_chat_participants(self, chat_id: UUID) -> list[UUID]:
        return await self.repository.get_chat_participants(chat_id)

    async def save_message(self, data: MessageCreate) -> MessageOut | None:
        created = await self.repository.create_message(data)
        if created is None:
            raise MessageFoundError(message="Couldn't create a message")
        return MessageOut(**created)

    async def mark_as_read(self, message_id: UUID) -> MessageOut | None:
        updated = await self.repository.update_message_read_status(message_id)
        if updated is None:
            raise MessageFoundError(message="Couldn't update message read status")
        return MessageOut(**updated)
