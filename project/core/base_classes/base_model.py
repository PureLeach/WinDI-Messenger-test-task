from datetime import datetime
from typing import Annotated

from humps import camelize
from pydantic import AwareDatetime as AwareDatetimeOriginal
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
)


class ProjectBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=camelize,
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
    )


def fix_postgres_datetime(v: str | datetime) -> str | datetime:
    """Workaround for https://github.com/pydantic/pydantic/issues/6576"""
    if isinstance(v, str) and "+" in v:
        dt, tz = v.split("+")
        if len(tz) == 2:  # noqa: PLR2004
            return f"{dt}+{tz}00"
    return v


PositiveInt32 = Annotated[int, Field(gt=0, le=2_147_483_647)]

ConstrainedName = Annotated[str, Field(max_length=256)]

AwareDatetime = Annotated[AwareDatetimeOriginal, BeforeValidator(fix_postgres_datetime)]
