from typing import Annotated

from fastapi import APIRouter, Depends

from project.modules.users.models import UserCreate, UserOut
from project.modules.users.repository import UserRepository
from project.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service() -> UserService:
    return UserService(UserRepository())


@router.post("/", summary="Create user")
async def create_user(user: UserCreate, service: Annotated[UserService, Depends(get_user_service)]) -> UserOut:
    return await service.register_user(user)
