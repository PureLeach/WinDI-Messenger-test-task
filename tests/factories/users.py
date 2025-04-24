import factory

from project.tables.users import users
from tests.factory_base import AsyncSQLAlchemyFactoryExtended, create_orm_model


class UserFactory(AsyncSQLAlchemyFactoryExtended):
    class Meta:
        model = create_orm_model(users)
        sqlalchemy_session = None

    id = factory.Faker("uuid4")
    name = factory.Faker("word")
    email = factory.Faker("email")
    password = factory.Faker("password")
