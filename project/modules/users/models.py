from uuid import UUID

from project.core.base_classes.base_model import ProjectBaseModel


class UserCreate(ProjectBaseModel):
    name: str
    email: str
    password: str


class UserOut(ProjectBaseModel):
    id: UUID
    name: str
    email: str
