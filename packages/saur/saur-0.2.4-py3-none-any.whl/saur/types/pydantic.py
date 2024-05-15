from __future__ import annotations
from typing import TYPE_CHECKING, Any
from sqlalchemy.types import TypeDecorator, JSON
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from pydantic import BaseModel
    from sqlalchemy.engine.interfaces import Dialect
    from sqlalchemy.types import TypeEngine


class ModeledJSON(TypeDecorator):
    impl = JSON

    def __init__(self, model: type[BaseModel], *, nullable: bool = True, **dump_kwargs):
        self.model = model
        self.nullable = nullable
        # enforce to mode: json for types like datetimes
        if "mode" in dump_kwargs and dump_kwargs["mode"] != "json":
            msg = "Must dump from Pydantic model in JSON mode in order to store in DB"
            raise ValueError(msg)
        self.dump_kwargs = dump_kwargs | {"mode": "json"}
        super().__init__()

    def model_validate(self, value: Any, **kwargs) -> BaseModel:
        # if isinstance(value, dict):
        #    return self.model.model_validate(value, **kwargs)
        return self.model.model_validate(value, **kwargs)

    def process_bind_param(self, value: Any, dialect: Dialect) -> dict[str, Any] | None:  # noqa: ARG002
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return self.model_validate(value).model_dump(**self.dump_kwargs)

    def process_result_value(self, value: Any, dialect: Dialect) -> BaseModel | None:  # noqa: ARG002
        if value is None:
            if self.nullable:
                return None
            msg = "Null value in non-nullable column"
            raise ValueError(msg)
        return self.model_validate(value)


class ModeledJSONB(ModeledJSON):
    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[JSONB | JSON]:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())
