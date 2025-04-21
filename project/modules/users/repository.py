from sqlalchemy import insert, select

from project.core.base_classes.base_model import PositiveInt32
from project.core.base_classes.base_repository import BaseRepository
from project.modules.users.models import UserCreateRequest, UserResponse
from project.tables.users import users


class UserRepository(BaseRepository):
    async def fetch_all_users(self) -> list[UserResponse]:
        query = select(users).order_by(users.c.id)
        rows = await self.db.fetch_all(query)
        return [UserResponse(**row._mapping) for row in rows]

    async def fetch_user(self, user_id: PositiveInt32) -> UserResponse | None:
        query = select(users).where(users.c.id == user_id)
        row = await self.db.fetch_one(query)
        if row:
            return UserResponse(**row._mapping)
        return None

    async def insert_user(self, user: UserCreateRequest) -> UserResponse | None:
        query = insert(users).values(user.model_dump()).returning(users)
        row = await self.db.fetch_one(query=query)
        if row:
            return UserResponse(**row._mapping)
        return None
