from project.core.base_classes.base_model import AwareDatetime, ConstrainedName, ProjectBaseModel


class UserCreateRequest(ProjectBaseModel):
    name: ConstrainedName


class UserResponse(ProjectBaseModel):
    id: int
    name: str
    created_at: AwareDatetime
    updated_at: AwareDatetime
    deleted: bool
