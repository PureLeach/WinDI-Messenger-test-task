from enum import Enum
from uuid import UUID

from project.core.base_classes.base_model import ProjectBaseModel


class ChatType(str, Enum):
    personal = "personal"
    group = "group"


class ChatCreate(ProjectBaseModel):
    name: str | None = None
    type: ChatType
    participant_ids: list[UUID]


class ChatOut(ProjectBaseModel):
    id: UUID
    name: str | None
    type: ChatType
    participant_ids: list[UUID]
