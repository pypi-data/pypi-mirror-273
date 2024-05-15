from __future__ import annotations
from typing import TYPE_CHECKING, Any
from datetime import datetime, timedelta, timezone, UTC

from sqlalchemy.types import TypeDecorator
from sqlalchemy import Integer, Float

if TYPE_CHECKING:
    from sqlalchemy import Dialect
    from sqlalchemy.sql.operators import OperatorType
    from sqlalchemy.types import TypeEngine


# as numeric b/c dateinterval logic is not supported by sqlalchemy across dialects
class FloatDateTime(TypeDecorator):
    impl = Float
    # python_type = datetime
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect: Dialect) -> float | None: # noqa: ARG002
        if value is None:
            return None
        # all datetimes are UTC
        return value.replace(tzinfo=timezone.utc).timestamp()

    def process_result_value(self, value: float | None, dialect: Dialect) -> datetime | None: # noqa: ARG002
        if value is None:
            return None
        # all datetimes are UTCtcfromtimestamp(value)
        return datetime.fromtimestamp(value, tz=UTC)

    def coerce_compared_value(self, op: OperatorType | None, value: Any) -> TypeEngine:
        return self.impl.coerce_compared_value(op, value)  # pyright: ignore[reportCallIssue]
        if isinstance(value, float):
            return Float()
        if isinstance(value, int):
            return Integer()
        return self

    def __repr__(self) -> str:
        return "FloatDateTime"


class IntDateTime(FloatDateTime):
    impl = Integer

    def process_bind_param(self, value: datetime | None, dialect: Dialect) -> int | None:
        result = super().process_bind_param(value, dialect)
        if result is None:
            return None
        return int(result)

    def __repr__(self) -> str:
        return "IntDateTime"


class FloatTimeDelta(TypeDecorator):
    impl = Float
    # python_type = timedelta
    cache_ok = True

    def process_bind_param(self, value: timedelta | float | None, dialect: Dialect) -> float | None: # noqa: ARG002
        if value is None:
            return None
        if isinstance(value, (float, int)):
            return value
        return timedelta.total_seconds(value)

    def process_result_value(self, value: float | None, dialect: Dialect) -> timedelta | None: # noqa: ARG002
        if value is None:
            return None
        return timedelta(seconds=value)

    def coerce_compared_value(self, op: OperatorType | None, value: Any) -> TypeEngine:
        return self.impl.coerce_compared_value(op, value)  # pyright: ignore[reportCallIssue]
        if isinstance(value, float):
            return Float()
        if isinstance(value, int):
            return Integer()
        return self

    def __repr__(self) -> str:
        return "FloatTimeDelta"


class IntTimeDelta(FloatTimeDelta):
    impl = Integer

    def process_bind_param(self, value: timedelta | float | None, dialect: Dialect) -> int | None:
        result = super().process_bind_param(value, dialect)
        if result is None:
            return None
        return int(result)

    def __repr__(self) -> str:
        return "IntTimeDelta"
