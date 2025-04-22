from uuid import UUID

from project.core.base_classes.base_model import ProjectBaseModel


class ChatCreate(ProjectBaseModel):
    name: str | None = None
    type: str
    participant_ids: list[UUID]


class ChatOut(ProjectBaseModel):
    id: UUID
    name: str | None
    type: str
    participant_ids: list[UUID]
