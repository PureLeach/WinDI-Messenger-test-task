from collections.abc import Mapping
from uuid import uuid4

from sqlalchemy import insert, select

from project.core.base_classes.base_repository import BaseRepository
from project.tables.users import users


class UserRepository(BaseRepository):
    async def create_user(self, name: str, email: str, password: str) -> dict | None:
        query = insert(users).values(name=name, email=email, password=password).returning(users)
        result = await self.db.fetch_one(query)
        return dict(result) if result else None

    async def get_user_by_email(self, email: str) -> Mapping | None:
        query = select(users).where(users.c.email == email)
        result = await self.db.fetch_one(query)
        return dict(result) if result else None
