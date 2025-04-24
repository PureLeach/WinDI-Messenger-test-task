from datetime import datetime

import factory

from project.tables.messages import messages
from tests.factories.chats import ChatFactory
from tests.factories.users import UserFactory
from tests.factory_base import AsyncSQLAlchemyFactoryExtended, create_orm_model


class MessageFactory(AsyncSQLAlchemyFactoryExtended):
    class Meta:
        model = create_orm_model(messages)
        sqlalchemy_session = None

    id = factory.Faker("uuid4")
    chat_id = factory.SubFactory(ChatFactory)
    sender_id = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence", nb_words=4)
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    read = factory.Faker("boolean", chance_of_getting_true=0)
