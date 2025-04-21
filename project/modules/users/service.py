from fastapi import HTTPException, status

from project.core.base_classes.base_model import PositiveInt32
from project.core.base_classes.base_service import BaseService
from project.modules.users.models import UserCreateRequest, UserResponse
from project.modules.users.repository import UserRepository


class UserService(BaseService):
    def __init__(self, repository: UserRepository | None = None) -> None:
        super().__init__()
        self.repository = repository or UserRepository()

    async def get_users(self) -> list[UserResponse]:
        return await self.repository.fetch_all_users()

    async def get_user(self, user_id: PositiveInt32) -> UserResponse:
        result = await self.repository.fetch_user(user_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return result

    async def create_user(self, user: UserCreateRequest) -> UserResponse:
        result = await self.repository.insert_user(user)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user",
            )
        return result
