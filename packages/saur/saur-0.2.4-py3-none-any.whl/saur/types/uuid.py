from __future__ import annotations
from typing import TYPE_CHECKING

# adapted from https://stackoverflow.com/a/30604002
# and from https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/uuid.html#UUIDType
import uuid

from sqlalchemy.types import TypeDecorator, BINARY, CHAR
from sqlalchemy.dialects import postgresql, mssql

if TYPE_CHECKING:
    from sqlalchemy import Dialect
    from sqlalchemy.types import TypeEngine


class UUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    BINARY(16), to store UUID.

    """

    impl = BINARY(16)
    # python_type = uuid.UUID
    cache_ok = True

    def __init__(self, *, binary: bool = True, native: bool = True):
        self.binary = binary
        self.native = native
        super().__init__()

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine:
        if self.native:
            if dialect.name in ("postgresql", "cockroachdb"):
                return dialect.type_descriptor(postgresql.UUID())
            if dialect.name == "mssql":
                return dialect.type_descriptor(mssql.UNIQUEIDENTIFIER())
        if self.binary:
            return dialect.type_descriptor(BINARY(16))
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(
        self, value: None | bytes | int | str | uuid.UUID, dialect: Dialect
    ) -> None | str | bytes:
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            if isinstance(value, (bytes, bytearray, memoryview)):
                value = uuid.UUID(bytes=value)
            elif isinstance(value, int):
                value = uuid.UUID(int=value)
            elif isinstance(value, str):
                value = uuid.UUID(value)
        if self.native and dialect.name in ("postgresql", "mssql", "cockroachdb"):
            return str(value)
        return value.bytes if self.binary else value.hex

    def process_result_value(
        self,
        value: None | str | bytes | uuid.UUID,
        dialect: Dialect,  # noqa: ARG002
    ) -> None | uuid.UUID:
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        # if self.native and dialect.name in ("postgresql", "mssql", "cockroachdb"):
        #    if isinstance(value, (bytes, bytearray, memoryview)):
        #        msg = "Must specify binary=True to allow bytes values"
        #        raise TypeError(msg)
        #    result = uuid.UUID(value)
        is_binary = isinstance(value, (bytes, bytearray, memoryview))
        if self.binary:
            if not is_binary:
                msg = "Must specify byte values with binary=True"
                raise TypeError(msg)
            return uuid.UUID(bytes=value)
        if is_binary:
            msg = "Must specify binary=True to allow bytes values"
            raise TypeError(msg)
        return uuid.UUID(value)
