from __future__ import annotations
from typing import TypeVar
from datetime import datetime, UTC


def utcnow() -> datetime:
    return datetime.now(UTC)


T = TypeVar("T")


def as_list(value: T | list[T]) -> list[T]:
    if isinstance(value, list):
        return value
    return [value]
