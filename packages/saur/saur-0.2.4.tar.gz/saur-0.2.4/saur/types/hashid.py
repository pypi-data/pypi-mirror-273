from __future__ import annotations
from typing import Self, TYPE_CHECKING

from sqlalchemy.types import TypeDecorator, Integer

import randseq

if TYPE_CHECKING:
    from sqlalchemy import Dialect


class StringInteger(TypeDecorator):
    # no-op type as fallback for undefined HashID
    impl = Integer
    # python_type = str
    cache_ok = True

    def __init__(self, *, nullable: bool = True):
        self.nullable = nullable
        super().__init__()

    def process_bind_param(self, value: str | None, dialect: Dialect) -> int | None:  # noqa: ARG002
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return int(value)

    def process_result_value(self, value: int | None, dialect: Dialect) -> str | None:  # noqa: ARG002
        if self.nullable and value is None:
            return None
        return str(value)


class HashID(TypeDecorator):
    impl = Integer
    # python_type = str
    cache_ok = True

    @classmethod
    def loads(cls, spec: str | None, *, nullable: bool = True) -> Self | StringInteger:
        if spec is None:
            return StringInteger(nullable=nullable)
        hashid = HashID.loads(spec)
        return cls(**hashid.to_dict(), nullable=nullable)

    def __init__(
        self, bound: int, init: int, prog: int, alphabet: str, outlen: int, *, nullable: bool = True
    ):
        self.hashid = randseq.HashID(
            bound=bound, init=init, prog=prog, alphabet=alphabet, outlen=outlen
        )
        self.nullable = nullable
        super().__init__()

    def process_bind_param(self, value: str | None, dialect: Dialect) -> int | None:  # noqa: ARG002
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return self.hashid.invert(value.encode())

    def process_result_value(self, value: int | None, dialect: Dialect) -> str | None:  # noqa: ARG002
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return self.hashid.hash(value).decode()
