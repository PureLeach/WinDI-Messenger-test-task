from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from project.modules.chats.models import ChatCreate, ChatOut
from project.modules.chats.repository import ChatRepository
from project.modules.chats.service import ChatService

router = APIRouter(prefix="/chats", tags=["Chats"])


def get_chat_service() -> ChatService:
    return ChatService(ChatRepository())


@router.post("/", summary="Create chat")
async def create_chat(chat: ChatCreate, service: Annotated[ChatService, Depends(get_chat_service)]) -> ChatOut:
    return await service.create_chat(chat)


@router.post("/chats/{chat_id}/users/{user_id}", summary="Add user to chat")
async def add_user_to_chat(
    chat_id: UUID, user_id: UUID, service: Annotated[ChatService, Depends(get_chat_service)]
) -> ChatOut:
    return await service.add_user_to_chat(chat_id, user_id)


@router.get("/", summary="Get chats for user")
async def get_chats_for_user(
    user_id: UUID, service: Annotated[ChatService, Depends(get_chat_service)]
) -> list[ChatOut]:
    return await service.get_chats_for_user(user_id)
