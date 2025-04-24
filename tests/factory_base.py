import factory
from sqlalchemy import insert, update
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def create_orm_model(table, pk=None, **kwargs):
    name = f"TemporaryORMModel_{table.name}"

    return type(
        name,
        (Base,),
        {
            "__table__": table,
            "__mapper_args__": {"primary_key": [getattr(table.c, pk)]} if pk else {},
        },
    )


class AsyncSQLAlchemyFactoryExtended(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    async def _create(cls, model_class, *_, **kwargs):
        database = kwargs.pop("database")
        query = insert(model_class).values(**kwargs).returning(*model_class.__table__.columns)
        result = await database.fetch_one(query)
        return model_class(**result._mapping)

    @classmethod
    async def update_fields(cls, *_, **kwargs):
        model_class = cls._meta.model
        database = kwargs.pop("database")
        query = update(model_class).values(**kwargs).returning(*model_class.__table__.columns)
        result = await database.fetch_one(query)
        return model_class(**result._mapping)
