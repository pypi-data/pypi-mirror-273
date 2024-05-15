from __future__ import annotations
from typing import TYPE_CHECKING, Any
from dateutil.relativedelta import relativedelta

from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel

if TYPE_CHECKING:
    from sqlalchemy import Dialect
    from sqlalchemy.types import TypeEngine


def not_private(attr: str) -> bool:
    return not attr.startswith("_")


class RelativeDeltaModel(BaseModel):
    years: int = 0
    months: int = 0
    days: int = 0
    leapdays: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    microseconds: int = 0
    year: int | None = None
    month: int | None = None
    day: int | None = None
    hour: int | None = None
    minute: int | None = None
    second: int | None = None
    microsecond: int | None = None
    weekday: int | None = None
    # _has_time: int ?

    def relativedelta(self) -> relativedelta:
        return relativedelta(**self.model_dump())


def _screen_values(delta: dict[str, int | None]) -> dict[str, int]:
    return {
        k: v
        for k, v in delta.items()
        if not (k.startswith("_") or v is None or (k.endswith("s") and v == 0))
    }


def serialize_relativedelta(delta: relativedelta | RelativeDeltaModel | dict) -> dict[str, int]:
    if isinstance(delta, relativedelta):
        return _screen_values(delta.__dict__)
    if isinstance(delta, RelativeDeltaModel):
        return _screen_values(delta.model_dump())
    if isinstance(delta, dict):
        return _screen_values(delta)
    msg = f"Unknown type for relativedelta: {type(delta)}"
    raise TypeError(msg)


def deserialize_relativedelta(delta: dict[str, int | None]) -> relativedelta:
    if "dt1" in delta or "dt2" in delta:
        msg = "Unsupported arguments"
        raise ValueError(msg)
    return relativedelta(**delta)  # pyright: ignore[reportArgumentType]


class RelativeDelta(TypeDecorator):
    impl = JSON
    # python_type = relativedelta
    cache_ok = True

    def __init__(self, *, nullable: bool = True):
        self.nullable = nullable
        super().__init__()

    def process_bind_param(
        self,
        value: relativedelta | RelativeDeltaModel | dict | None,
        dialect: Dialect,  # noqa: ARG002
    ) -> None | dict[str, int]:
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return serialize_relativedelta(value)

    def process_result_value(
        self,
        value: dict[str, int | None] | None,
        dialect: Dialect,  # noqa: ARG002
    ) -> relativedelta | None:
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return deserialize_relativedelta(value)


class RelativeDeltaB(RelativeDelta):
    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())
