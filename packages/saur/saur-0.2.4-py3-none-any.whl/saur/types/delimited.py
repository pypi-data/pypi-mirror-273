# adapted from https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/scalar_list.html#ScalarListType
from __future__ import annotations
from typing import TYPE_CHECKING, Callable, TypeVar, Generic

from sqlalchemy.types import UnicodeText, TypeDecorator

if TYPE_CHECKING:
    from sqlalchemy import Dialect

# commonly used delimiter
DELETE_CHARACTER = "\x7f"

T = TypeVar("T")


# pass-through for type checking
def str_noop(value: str) -> str:
    return value


class DelimitedList(TypeDecorator, Generic[T]):
    impl = UnicodeText()
    cache_ok = True

    def __init__(
        self,
        serialize: Callable[[T], str] = str_noop,
        deserialize: Callable[[str], T] = str_noop,
        separator: str = ",",
    ):
        self.separator = separator
        self.serialize = serialize
        self.deserialize = deserialize
        super().__init__()

    def process_bind_param(self, value: list[T] | None, dialect: Dialect) -> str | None:  # noqa: ARG002
        if value is None:
            return None

        serialized_values = [self.serialize(val) for val in value]
        invalid_values = [val for val in serialized_values if self.separator in val]
        if invalid_values:
            msg = f"Delimited values {invalid_values!r} cannot contain seperator {self.separator!r}"
            raise ValueError(msg)
        return self.separator.join(serialized_values)

    def process_result_value(self, value: str | None, dialect: Dialect) -> list[T] | None:  # noqa: ARG002
        if value is None:
            return None
        if not value:
            return []
        return [self.deserialize(val) for val in value.split(self.separator)]
