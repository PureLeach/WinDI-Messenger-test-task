import factory

from project.modules.chats.models import ChatType
from project.tables.chats import chats
from tests.factory_base import AsyncSQLAlchemyFactoryExtended, create_orm_model


class ChatFactory(AsyncSQLAlchemyFactoryExtended):
    class Meta:
        model = create_orm_model(chats)
        sqlalchemy_session = None

    id = factory.Faker("uuid4")
    name = factory.Faker("word")
    type = factory.Faker("random_element", elements=list(ChatType))
