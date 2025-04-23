from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from project.config.base import settings
from project.modules.message.handlers import process_incoming_event
from project.modules.message.models import MessageOut
from project.modules.message.repository import MessageRepository
from project.modules.message.service import MessageService
from project.modules.message.ws_manager import manager

logger = settings.LOGGER.getChild(__name__)
router = APIRouter(prefix="/messages", tags=["Messages"])


def get_message_service() -> MessageService:
    return MessageService(MessageRepository())


@router.get("/history/{chat_id}", summary="Get message history")
async def get_history(
    chat_id: UUID,
    service: Annotated[MessageService, Depends(get_message_service)],
    limit: int = 100,
    offset: int = 0,
) -> list[MessageOut]:
    return await service.get_history(chat_id, limit, offset)


@router.websocket("/ws/{chat_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: UUID,
    user_id: UUID,
    service: Annotated[MessageService, Depends(get_message_service)],
) -> None:
    try:
        await websocket.accept()
        if not await service.validate_connection(chat_id, user_id):
            await websocket.close(code=1008, reason="Invalid connection")
            return

        await manager.connect(chat_id, user_id, websocket)

        while True:
            raw_data = await websocket.receive_json()
            await process_incoming_event(websocket, service, raw_data, chat_id, user_id)

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: chat_id={chat_id}, user_id={user_id}")
        manager.disconnect(chat_id, user_id)
    except RuntimeError as e:
        logger.error(f"Connection error: {e}")
        await websocket.close(code=1011, reason="Internal server error")
        manager.disconnect(chat_id, user_id)
