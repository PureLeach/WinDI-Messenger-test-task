from fastapi import HTTPException, status

from project.modules.users.models import UserCreate, UserOut
from project.modules.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_user(self, user_data: UserCreate) -> UserOut:
        created_user = await self.repository.create_user(user_data.name, user_data.email, user_data.password)
        if created_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user")
        return UserOut(**created_user)
