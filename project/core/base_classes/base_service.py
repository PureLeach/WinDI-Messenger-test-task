from project.config.base import settings
from project.core.base_classes.base_repository import BaseRepository


class BaseService:
    ds: BaseRepository

    def __init__(self) -> None:
        self.logger = settings.LOGGER.getChild(self.__class__.__name__)
