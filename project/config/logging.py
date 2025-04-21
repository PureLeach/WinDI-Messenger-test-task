from pydantic_settings import BaseSettings


class LoggingConfig(BaseSettings):
    DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"
    FORMAT: str = "%(asctime)s %(levelname)s %(name)s: [%(message)s]"
    FORMAT_WITH_CONTEXT: str = (
        "%(asctime)s %(levelname)s %(name)s: [%(message)s] "
        "request_id=%(request_id)s user_id=%(user_id)s session=%(session)s"
    )
    LEVEL: str = "INFO"
