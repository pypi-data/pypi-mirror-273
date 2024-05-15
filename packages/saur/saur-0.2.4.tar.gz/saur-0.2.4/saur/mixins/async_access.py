from __future__ import annotations
from typing import Self, Any, Collection, TYPE_CHECKING, ClassVar
from asyncio import gather
from functools import cache
from dataclasses import dataclass

from inspect import getmembers_static

from sqlalchemy import inspect, Column, update
from sqlalchemy.orm import selectinload, QueryableAttribute, declarative_mixin
from sqlalchemy.sql.expression import select, Select, delete, and_, literal
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.hybrid import hybrid_property

try:
    from cytoolz import keyfilter  # pyright: ignore[reportAttributeAccessIssue]
except ImportError:
    from toolz import keyfilter

__all__ = ["AsyncAccessMixin"]

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.engine import ScalarResult
    from sqlalchemy.sql.expression import ColumnElement, Delete
    from sqlalchemy.orm import Mapper, InstanceState


def is_property(obj: Any) -> bool:
    return isinstance(obj, (property, hybrid_property))


SelectFieldType = QueryableAttribute | Collection[QueryableAttribute]


def select_fields(query: Select, fields: Collection[SelectFieldType]) -> Select:
    if not fields:
        return query
    options = []
    for field in fields:
        if isinstance(field, QueryableAttribute):
            option = selectinload(field)
        elif not field:
            continue
        else:
            field_iter = iter(field)
            option = selectinload(next(field_iter))
            for step in field_iter:
                option = option.selectinload(step)
        options.append(option)
    return query.options(*options)


@dataclass
class CorrelateField:
    field: str
    on: Collection[str]
    model: type[AsyncAccessMixin]
    fetch: bool = False
    force: bool = False


class CorrelateError(RuntimeError):
    pass


@declarative_mixin
class AsyncAccessMixin:
    correlate_fields: ClassVar[tuple[str | CorrelateField, ...]] = ()
    # later: auto-rewrite all varkwargs signatures with model fields

    @classmethod
    @cache
    def _mapper(cls) -> Mapper:
        return inspect(cls)  # pyright: ignore[reportReturnType]

    def _state(self) -> InstanceState:
        return inspect(self)  # pyright: ignore[reportReturnType]

    @classmethod
    @cache
    def _primary_keys(cls) -> tuple[Column, ...]:
        return cls._mapper().primary_key

    def pks(self) -> tuple:
        return tuple(getattr(self, pk.name) for pk in self._primary_keys())

    @classmethod
    @cache
    def _relationships(cls) -> dict[str, type[AsyncAccessMixin]]:
        return {rel.key: rel.entity.class_ for rel in cls._mapper().relationships}

    @classmethod
    @cache
    def _correlate_fields(cls) -> dict[str, CorrelateField]:
        result = {}
        for cf_spec in cls.correlate_fields:
            if isinstance(cf_spec, str):
                field = cf_spec
                try:
                    model = cls._relationships()[field]
                except KeyError as exc:
                    msg = f"Cannot find relationship {field} on {cls.__name__}"
                    raise RuntimeError(msg) from exc
                on = tuple(pk.name for pk in model._primary_keys())  # noqa: SLF001
                cf = CorrelateField(field, on=on, model=model)
            else:
                cf = cf_spec
            result[cf.field] = cf
        return result

    # @cachedproperty desired, but error:
    # `Cannot use cached_property instance without calling __set_name__ on it.`
    @classmethod
    @cache
    def _field_names(cls) -> set[str]:
        orm_props = {prop.key for prop in cls._mapper().iterate_properties}
        py_props = {
            name for (name, _) in getmembers_static(cls, is_property) if not name.startswith("_")
        }
        return orm_props | py_props

    def to_dict(self, fields: Collection[str] | None = None) -> dict[str, Any]:
        if fields is None:
            return keyfilter(self._field_names().__contains__, self.__dict__)
        return {k: getattr(self, k) for k in fields}

    # basic queries

    @classmethod
    def select(cls, *with_fields: SelectFieldType, **filters) -> Select:
        # with_fields as QueryableAttribute or list/tuple[QueryableAttribute]
        #  - in latter: selectinload chain
        query = select_fields(select(cls), with_fields)
        if filters:
            query = query.filter_by(**filters)
        return query

    @classmethod
    def select_pk(cls, primary_key: Any, /, *with_fields: SelectFieldType, **filters) -> Select:
        if isinstance(primary_key, (tuple, list)):
            pk_fields = cls._primary_keys()
            if len(pk_fields) != len(primary_key):
                msg = "pk must be the same length as the number of primary keys on model"
                raise ValueError(msg)
            for pk_field, pk_value in zip(pk_fields, primary_key, strict=True):
                filters[pk_field.name] = pk_value
        else:
            try:
                (pk_field,) = cls._primary_keys()
            except TypeError as exc:
                msg = "Can only use pk shorthand for single-pk models"
                raise TypeError(msg) from exc
            filters[pk_field.name] = primary_key
        return cls.select(*with_fields, **filters)

    @classmethod
    def where(cls, **filters) -> ColumnElement:
        collect = []
        for key, value in filters.items():
            attr = getattr(cls, key)
            collect.append(attr == value)
        return and_(*collect)

    # exists utility

    @classmethod
    async def exists(cls, *, session: AsyncSession, **filters) -> bool:
        query = select(literal(True)).filter_by(**filters).limit(1)  # noqa: FBT003
        result = (await session.execute(query)).scalar_one_or_none()
        return bool(result)

    # basic get

    @classmethod
    async def find(
        cls, *with_fields: SelectFieldType, session: AsyncSession, **filters
    ) -> ScalarResult[Self]:
        query = cls.select(*with_fields, **filters)
        return await session.scalars(query)

    @classmethod
    async def find_one(
        cls, *with_fields: SelectFieldType, session: AsyncSession, **filters
    ) -> Self:
        query = cls.select(*with_fields, **filters)
        result = await session.execute(query)
        return result.scalar_one()

    @classmethod
    async def get(
        cls, primary_key: Any, /, *with_fields: SelectFieldType, session: AsyncSession, **filters
    ) -> Self:
        query = cls.select_pk(primary_key, *with_fields, **filters)
        result = await session.execute(query)
        return result.scalar_one()

    async def with_fields(
        self, *with_fields: str, session: AsyncSession, force: bool = False
    ) -> Self:
        # later: nested with fields (with_fields: str | Collection[str])
        # via https://github.com/sqlalchemy/sqlalchemy/discussions/10908#discussioncomment-8202598
        # ie https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.get.params.populate_existing
        # (should also use for get ??)
        unloaded = self._state().unloaded
        if (set(with_fields) & set(unloaded)) or force:
            await session.refresh(self, attribute_names=with_fields)
        return self

    # create - update - delete (& upsert)

    @classmethod
    async def create(
        cls, *, session: AsyncSession, commit: bool = True, refresh: bool = True, **kwargs
    ) -> Self:
        for field_name, field_spec in cls._correlate_fields().items():
            if field_name in kwargs:
                kwargs[field_name] = await field_spec.model.batch_create(
                    kwargs[field_name], session=session, commit=False
                )
        new_obj = cls(**kwargs)
        session.add(new_obj)
        if commit:
            await session.commit()
            if refresh:
                await session.refresh(new_obj)
        return new_obj

    @classmethod
    async def create_if_not_exists(cls, *, session: AsyncSession, **kwargs) -> Self:
        existing = await cls.find(session=session, **kwargs)
        try:
            return existing.one()
        except NoResultFound:
            new_obj = await cls.create(session=session, **kwargs)
            await session.commit()
            await session.refresh(new_obj)
            return new_obj

    @classmethod
    async def upsert(
        cls,
        data: dict[str, Any],
        on: Collection[str],
        create_fields: Collection[str] | None = None,
        update_fields: Collection[str] | None = None,
        *,
        session: AsyncSession,
        commit: bool = True,
        refresh: bool = True,
    ) -> Self:
        # later: single statement upsert
        # https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-enabled-insert-update-and-delete-statements
        if create_fields is None:
            create_fields = on
        if update_fields is None:
            update_fields = set(data.keys()) - set(on)
        on_data = keyfilter(on.__contains__, data)
        existing_results = await cls.find(session=session, **on_data)
        try:
            obj = existing_results.one()
        except NoResultFound:
            create_data = keyfilter(create_fields.__contains__, data)
            obj = await cls.create(session=session, commit=commit, refresh=refresh, **create_data)
        if update_fields:
            update_data = keyfilter(update_fields.__contains__, data)
            await obj.update(session=session, commit=commit, refresh=refresh, **update_data)
        return obj

    @classmethod
    async def multiupsert(
        cls,
        rows: list[dict[str, Any]],
        on: Collection[str],
        create_fields: Collection[str] | None,
        update_fields: Collection[str] | None,
    ) -> None:
        pass

    async def update(
        self, *, session: AsyncSession, commit: bool = True, refresh: bool = True, **kwargs
    ) -> Self:
        for field_name, field_spec in self._correlate_fields().items():
            if field_name in kwargs:
                kwargs[field_name] = await self.correlate_field(
                    field_name,
                    kwargs[field_name],
                    model=field_spec.model,
                    on=field_spec.on,
                    force=field_spec.force,
                    fetch=field_spec.fetch,
                    session=session,
                )
        for key, value in kwargs.items():
            if key not in self._field_names():
                msg = f"Field {key} not settable."
                raise AttributeError(msg)
            setattr(self, key, value)
        session.add(self)
        if commit:
            await session.commit()
            if refresh:
                await session.refresh(self)
        return self

    async def delete(self, *, session: AsyncSession, commit: bool = True) -> None:
        await session.delete(self)
        if commit:
            await session.commit()

    # batch crud

    @classmethod
    async def batch_create(
        cls,
        data: Collection[dict[str, Any]],
        *,
        session: AsyncSession,
        commit: bool = True,
        refresh: bool = False,
        **addl_data,
    ) -> list[Self]:
        # included for api consistency
        results = await gather(
            *[cls.create(session=session, commit=False, **datum, **addl_data) for datum in data]
        )
        if commit:
            await session.commit()
            if refresh:
                for result in results:
                    await session.refresh(result)
        return results

    @classmethod
    async def batch_upsert(
        cls,
        data: Collection[dict[str, Any]],
        on: Collection[str],
        *,
        create_fields: Collection[str] | None = None,
        update_fields: Collection[str] | None = None,
        session: AsyncSession,
        commit: bool = True,
        refresh: bool = False,
    ) -> list[Self]:
        with session.no_autoflush:
            results = [
                await cls.upsert(
                    datum,
                    on,
                    session=session,
                    commit=False,
                    create_fields=create_fields,
                    update_fields=update_fields,
                )
                for datum in data
            ]
        if commit:
            await session.commit()
            if refresh:
                for result in results:
                    await session.refresh(result)
        return results

    @classmethod
    async def batch_update(
        cls, where: dict[str, Any], values: dict[str, Any], *, session: AsyncSession
    ) -> None:
        statement = (
            update(cls)
            .where(and_(*[getattr(cls, k) == v for k, v in where.items()]))
            .values(**values)
        )
        await session.execute(statement)

    @classmethod
    def batch_delete_query(cls, whereclause: ColumnElement | None = None, **filters) -> Delete:
        query = delete(cls)
        if whereclause is not None:
            query = query.where(whereclause)
        if filters:
            query = query.where(cls.where(**filters))
        return query

    @classmethod
    async def batch_delete(
        cls,
        whereclause: ColumnElement | None = None,
        *,
        session: AsyncSession,
        is_delete_using: bool = False,
        verbose: bool = False,
        **filters,
    ) -> None:
        query = cls.batch_delete_query(whereclause, **filters)
        exec_options = {}
        if is_delete_using:
            exec_options["is_delete_using"] = True
        if verbose:
            print(query)
        await session.execute(query, execution_options=exec_options)

    # correlating lists of objects

    async def correlate_field(
        self,
        field: str,
        data: list[dict],
        *,
        model: type[AsyncAccessMixin] | None = None,
        on: Collection[str] | None = None,
        fetch: bool = False,
        force: bool = False,
        session: AsyncSession,
    ) -> list[AsyncAccessMixin]:
        "A pattern for updating children models, which are fully dependent on the parent model."
        # if fetch, then try to find an object if it's not already populated
        # if not force, then only look for an object in already connected objs
        # if force, then create data obj if they aren't found
        # if not force, then only create data obj if they have some null key or if not fetch

        # fetch default for correlate from class var if it exists
        if model is None:
            try:
                model = self._correlate_fields()[field].model
            except KeyError:
                try:
                    model = self._relationships()[field]
                except KeyError as exc:
                    msg = f"Cannot find relationship {field} on {type(self).__name__}"
                    raise CorrelateError(msg) from exc
        if on is None:
            try:
                on = self._correlate_fields()[field].on
            except KeyError:
                on = tuple(pk.name for pk in model._primary_keys())  # noqa: SLF001

        await self.with_fields(field, session=session)
        existing = getattr(self, field)
        existing_by_key = {
            tuple(getattr(obj, on_field) for on_field in on): obj for obj in existing
        }
        results = []
        to_create = []
        for datum in data:
            datum_key = tuple(datum.get(on_field) for on_field in on)
            datum_obj = None
            if not any(key_val is None for key_val in datum_key):
                if datum_key in existing_by_key or (not fetch and not force):
                    datum_obj = existing_by_key[datum_key]
                elif fetch:
                    try:
                        datum_obj = await model.find_one(
                            session=session, **dict(zip(on, datum_key))
                        )
                        # datum_obj = await model.get(datum_key, session=session)
                    except NoResultFound as exc:
                        if not force:
                            # by default, raise an error if a non-null key does not exist
                            #  use force to create a new obj even when all the keys are specified
                            msg = f"Could not find {datum_key} on {model.__name__}"
                            raise CorrelateError(msg) from exc
            if datum_obj:
                results.append(await datum_obj.update(**datum, session=session, commit=False))
            else:
                to_create.append(datum)
        if to_create:
            results.extend(await model.batch_create(to_create, session=session, commit=False))
        return results

    @classmethod
    async def _correlate(
        cls,
        objs: list[Self],
        data: list[dict[str, Any]],
        on: Collection[str],
        *,
        update_fields: Collection[str] | None = None,
        session: AsyncSession,
        commit: bool = True,
        refresh: bool = True,
        **addl_data,
    ) -> tuple[list[dict], list[Self], list[Self]]:
        results = []
        to_create = []
        unseen = list(objs)
        for datum in data:
            for obj in unseen:
                if all(getattr(obj, k) == datum.get(k) for k in on):
                    results.append(obj)
                    unseen.remove(obj)
                    if update_fields is None:
                        to_update = (set(datum.keys()) | set(addl_data.keys())) - set(on)
                    else:
                        to_update = update_fields
                    if to_update:
                        obj_update = {}
                        for k in to_update:
                            existing = getattr(obj, k, None)
                            new = datum.get(k) if k in datum else addl_data.get(k)
                            if new != existing:
                                obj_update[k] = new
                        if obj_update:
                            await obj.update(**obj_update, commit=False, session=session)
                    break
            else:
                to_create.append(datum)
        if commit:
            await session.commit()
            if refresh:
                for result in results:
                    await session.refresh(result)
        return to_create, unseen, results

    @classmethod
    async def correlate(
        cls,
        objs: list[Self],
        data: list[dict] | list[Self],
        on: Collection[str],
        *,
        update_fields: Collection[str] | None = None,
        commit: bool = True,
        refresh: bool = False,
        session: AsyncSession,
        **addl_data,
    ) -> list[Self]:
        if all(isinstance(datum, cls) for datum in data):
            # short-circuit if already correlated
            return data  # pyright: ignore[reportReturnType]
        if not all(isinstance(datum, dict) for datum in data):
            msg = "Data cannot be mixed dicts and classes"
            raise TypeError(msg)
        to_create, _, results = await cls._correlate(
            objs,
            data,  # pyright: ignore[reportArgumentType]
            on,
            update_fields=update_fields,
            session=session,
            commit=commit,
            refresh=refresh,
            **addl_data,
        )
        if to_create:
            results.extend(
                await cls.batch_create(
                    to_create, session=session, commit=commit, refresh=refresh, **addl_data
                )
            )
        return results
