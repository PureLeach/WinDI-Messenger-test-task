import factory

from project.tables.group_participants import group_participant
from tests.factories.chats import ChatFactory
from tests.factories.users import UserFactory
from tests.factory_base import AsyncSQLAlchemyFactoryExtended, create_orm_model


class GroupParticipantFactory(AsyncSQLAlchemyFactoryExtended):
    class Meta:
        model = create_orm_model(group_participant)
        sqlalchemy_session = None

    chat_id = factory.SubFactory(ChatFactory)
    user_id = factory.SubFactory(UserFactory)
