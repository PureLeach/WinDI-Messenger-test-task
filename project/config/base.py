import logging

from pydantic_settings import BaseSettings

from project.config.db import DBConfig
from project.config.logging import LoggingConfig


class Settings(BaseSettings):
    DEBUG: bool = True
    PROJECT_NAME: str = "Messenger-test-task"

    DB: DBConfig = DBConfig()

    LOGGING: LoggingConfig = LoggingConfig()
    LOGGER: logging.Logger = logging.getLogger("Messenger")


settings = Settings()
