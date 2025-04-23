from collections.abc import Awaitable, Callable
from uuid import UUID

from fastapi import WebSocket
from pydantic import ValidationError

from project.config.base import settings
from project.modules.message.exception import MessageFoundError
from project.modules.message.models import (
    MessageCreate,
    MessageEvent,
    ReadEvent,
    WebSocketEventType,
    ws_event_adapter,
)
from project.modules.message.service import MessageService
from project.modules.message.ws_manager import manager

logger = settings.LOGGER.getChild(__name__)


async def process_incoming_event(
    websocket: WebSocket,
    service: MessageService,
    raw_data: dict,
    chat_id: UUID,
    user_id: UUID,
) -> None:
    try:
        event = ws_event_adapter.validate_python(raw_data)
        handler = event_handlers.get(event.event)
        if handler:
            await handler(event, service, chat_id, user_id)
        else:
            await websocket.send_json({"error": f"Unknown event: {event.event}"})
    except ValidationError as ve:
        logger.error(f"Validation error: {ve.errors()}")
        await websocket.send_json({"error": "Invalid format", "details": ve.errors()})
    except (TypeError, ValueError, MessageFoundError) as e:
        logger.error(f"Processing error: {e}")
        await websocket.send_json({"error": "Invalid data", "details": str(e)})


async def handle_message(event: MessageEvent, service: MessageService, chat_id: UUID, user_id: UUID) -> None:
    saved_message = await service.save_message(MessageCreate(chat_id=chat_id, sender_id=user_id, text=event.data.text))
    if saved_message:
        await manager.broadcast_to_chat(chat_id, saved_message.model_dump(mode="json"))


async def handle_read(event: ReadEvent, service: MessageService, chat_id: UUID, _: UUID) -> None:
    updated_message = await service.mark_as_read(event.data.message_id)
    if updated_message:
        await manager.broadcast_to_chat(chat_id, updated_message.model_dump(mode="json"))


event_handlers: dict[WebSocketEventType, Callable[..., Awaitable[None]]] = {
    WebSocketEventType.MESSAGE: handle_message,
    WebSocketEventType.READ: handle_read,
}
