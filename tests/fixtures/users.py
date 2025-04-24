import pytest

from tests.factories.users import UserFactory


@pytest.fixture
async def create_users(db):
    user_1 = await UserFactory.create(database=db)
    user_2 = await UserFactory.create(database=db)
    user_3 = await UserFactory.create(database=db)
    return user_1, user_2, user_3
