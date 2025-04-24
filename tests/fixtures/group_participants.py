import pytest

from tests.factories.group_participants import GroupParticipantFactory


@pytest.fixture
async def create_group_participants(db, create_users, create_chats):
    await GroupParticipantFactory.create(database=db, chat_id=create_chats[0].id, user_id=create_users[0].id)
    await GroupParticipantFactory.create(database=db, chat_id=create_chats[0].id, user_id=create_users[1].id)
