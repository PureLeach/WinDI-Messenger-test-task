from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import Field, TypeAdapter

from project.core.base_classes.base_model import AwareDatetime, ProjectBaseModel


class MessageCreate(ProjectBaseModel):
    chat_id: UUID
    sender_id: UUID
    text: str


class MessageOut(ProjectBaseModel):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    text: str
    read: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime


class WebSocketEventType(str, Enum):
    MESSAGE = "message"
    READ = "read"


class MessageData(ProjectBaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class ReadData(ProjectBaseModel):
    message_id: UUID


class MessageEvent(ProjectBaseModel):
    event: Literal[WebSocketEventType.MESSAGE]
    data: MessageData


class ReadEvent(ProjectBaseModel):
    event: Literal[WebSocketEventType.READ]
    data: ReadData


ws_event_adapter: TypeAdapter[MessageEvent | ReadEvent] = TypeAdapter(MessageEvent | ReadEvent)
