"""Handle of unique ids."""

import typing

import ulid
import ulid.codec
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema

# UniqueId = ulid.ULID

UniqueIdPrimitive = ulid.api.api.ULIDPrimitive
# UniqueIdPrimitive = typing.Union[ulid.api.api.ULIDPrimitive, UniqueIdStr]


class UniqueId(ulid.ULID):  # noqa: D101
    @classmethod
    def __get_pydantic_json_schema__(  # noqa: D105, PLW3201
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, typing.Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)  # type: ignore [misc]
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(examples=["01BJQMF54D093DXEAWZ6JYRPAQ"])
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(  # noqa: D105, PLW3201
        cls, source: typing.Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        from_any_schema = core_schema.chain_schema(
            [
                core_schema.any_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]
        )
        return core_schema.json_or_python_schema(
            json_schema=from_any_schema,
            python_schema=core_schema.union_schema(
                [core_schema.is_instance_schema(ulid.ULID), from_any_schema]
            ),
        )

    @classmethod
    def validate(cls, v) -> "UniqueId":  # noqa: D102
        if isinstance(v, UniqueId):
            return v  # type: ignore
        if isinstance(v, ulid.ULID):
            return v  # type: ignore
        if not isinstance(v, UniqueIdPrimitive):  # type: ignore
            msg = f"Unsupported type ('{type(v)}')"
            raise TypeError(msg)
        try:
            return ulid.parse(v)  # type: ignore
        except ValueError as err:
            msg = "not a valid ULID"
            raise ValueError(msg) from err

    def __repr__(self) -> str:  # noqa: D105
        return f"UniqueId({super().__repr__()})"


UniqueIdType = (ulid.ULID, UniqueId)


def make_unique_id(
    t: ulid.codec.TimestampPrimitive | None = None,
) -> UniqueId:
    """Generate an UniqueId that are sortable.

    >>> from karp_lex_types.value_objects import make_unique_id
    >>> from datetime import datetime
    >>> old_id = make_unique_id(datetime(1999,12,31,23,59,59))
    >>> make_unique_id() > old_id
    True
    """
    return ulid.new() if t is None else ulid.from_timestamp(t)  # type: ignore


parse = ulid.parse

LEN_OF_ULID: int = 26


class UniqueIdStr(str):  # noqa: D101
    @classmethod
    def __get_pydantic_json_schema__(  # noqa: D105, PLW3201
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, typing.Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)  # type: ignore [misc]
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(examples=["01BJQMF54D093DXEAWZ6JYRPAQ"])
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(  # noqa: D105, PLW3201
        cls, source: typing.Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_before_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v, _info):  # noqa: D102
        if isinstance(v, UniqueId | ulid.ULID):
            return str(v)
        if not isinstance(v, str):
            raise TypeError("string or UniqueId required")

        if len(v) != LEN_OF_ULID:
            raise ValueError("invalid uniqueid format")

        return cls(v)

    def __repr__(self) -> str:  # noqa: D105
        return f"UniqueIdStr({super().__repr__()})"
