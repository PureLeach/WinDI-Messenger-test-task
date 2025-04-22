from typing import Annotated

from fastapi import APIRouter, Depends

from project.modules.chats.models import ChatCreate, ChatOut
from project.modules.chats.repository import ChatRepository
from project.modules.chats.service import ChatService

router = APIRouter(prefix="/chats", tags=["Chats"])


def get_chat_service() -> ChatService:
    return ChatService(ChatRepository())


@router.post("/")
async def create_chat(chat: ChatCreate, service: Annotated[ChatService, Depends(get_chat_service)]) -> ChatOut:
    return await service.create_chat(chat)
