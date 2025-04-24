import pytest

from tests.factories.messages import MessageFactory


@pytest.fixture
async def create_messages(db, create_users, create_chats):
    await MessageFactory.create(database=db, chat_id=create_chats[0].id, sender_id=create_users[0].id)
    await MessageFactory.create(database=db, chat_id=create_chats[0].id, sender_id=create_users[0].id)
    await MessageFactory.create(database=db, chat_id=create_chats[0].id, sender_id=create_users[0].id)
    await MessageFactory.create(database=db, chat_id=create_chats[0].id, sender_id=create_users[0].id)
