from datetime import datetime  # noqa: D100
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, model_validator

from karp_lex_types import alias_generators
from karp_lex_types.value_objects import UniqueIdStr

T = TypeVar("T")


class GenericEntryDto(BaseModel, Generic[T]):  # noqa: D101
    entry: T
    last_modified_by: str | None = None
    last_modified: datetime | None = None
    id: UniqueIdStr | None = None
    version: int | None = None
    resource: str | None = None
    message: str | None = None
    discarded: bool = False
    model_config = ConfigDict(alias_generator=alias_generators.to_lower_camel)

    @model_validator(mode="before")
    @classmethod
    def allow_snake_case(cls, values):  # noqa: D102
        if "last_modified" in values:
            values["lastModified"] = values.pop("last_modified")
        if "last_modified_by" in values:
            values["lastModifiedBy"] = values.pop("last_modified_by")
        if "entity_id" in values:
            values["entityId"] = values.pop("entity_id")
        return values

    def serialize(self):  # noqa: D102
        return self.model_dump(by_alias=True, exclude_none=True)


class EntryDto(GenericEntryDto[dict]):  # noqa: D101
    ...
