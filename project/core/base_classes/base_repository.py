import traceback
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, TypeVar

from databases.core import Transaction

from project.config.base import settings
from project.core.base_classes.base_model import ProjectBaseModel

if TYPE_CHECKING:
    from databases import Database

ResponseModelType = TypeVar("ResponseModelType", bound=ProjectBaseModel)


class BaseRepository:
    def __init__(self) -> None:
        self.db: Database = settings.DB.db_instance
        self.logger = settings.LOGGER.getChild(self.__class__.__name__)

    @asynccontextmanager
    async def transaction(self, isolation: str | None = None) -> AsyncGenerator[Transaction, None]:
        current_transaction = self.db.transaction(isolation=isolation) if isolation else self.db.transaction()

        try:
            yield await current_transaction.start()
        except Exception as error:
            self.logger.error(f"Transaction failed: {error}")
            self.logger.error(traceback.print_exception(error))
            await current_transaction.rollback()
            raise error
        else:
            await current_transaction.commit()
