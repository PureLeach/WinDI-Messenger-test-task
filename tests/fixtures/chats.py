import pytest

from tests.factories.chats import ChatFactory


@pytest.fixture
async def create_chats(db):
    chat_1 = await ChatFactory.create(database=db)
    chat_2 = await ChatFactory.create(database=db)
    return chat_1, chat_2
