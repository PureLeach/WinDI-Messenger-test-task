from uuid import UUID

from pydantic import EmailStr

from project.core.base_classes.base_model import ProjectBaseModel


class UserCreate(ProjectBaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(ProjectBaseModel):
    id: UUID
    name: str
    email: EmailStr
