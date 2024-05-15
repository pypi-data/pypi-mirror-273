"""Entry commands."""

from collections.abc import Iterable
from typing import (
    Annotated,
    Generic,
    Literal,
    TypeVar,
)

import pydantic

from karp_lex_types.value_objects import UniqueId, make_unique_id

from .base import Command

T = TypeVar("T")


class GenericAddEntry(Command, Generic[T]):  # noqa: D101
    id: UniqueId = pydantic.Field(default_factory=make_unique_id)
    resource_id: str
    entry: T
    message: str
    cmdtype: Literal["add_entry"] = "add_entry"


class AddEntry(GenericAddEntry[dict]):
    """Command to add an entry."""


class AddEntries(Command):  # noqa: D101
    resource_id: str
    entries: Iterable[dict]
    message: str
    chunk_size: int = 0


class AddEntriesInChunks(AddEntries):  # noqa: D101
    chunk_size: int


class DeleteEntry(Command):  # noqa: D101
    resource_id: str
    id: UniqueId
    version: int
    message: str | None = None
    cmdtype: Literal["delete_entry"] = "delete_entry"


class ImportEntries(AddEntries):  # noqa: D101
    pass


class ImportEntriesInChunks(AddEntriesInChunks):  # noqa: D101
    pass


class GenericUpdateEntry(Command, Generic[T]):  # noqa: D101
    resource_id: str
    id: UniqueId
    version: int
    entry: T
    message: str
    force: bool = False
    cmdtype: Literal["update_entry"] = "update_entry"


class UpdateEntry(GenericUpdateEntry[dict]):  # noqa: D101
    ...


EntryCommandType = Annotated[
    AddEntry | DeleteEntry | UpdateEntry, pydantic.Field(discriminator="cmdtype")
]


class EntryCommand(pydantic.BaseModel):
    """A common class for Entry commands."""

    cmd: EntryCommandType


class ExecuteBatchOfEntryCommands(pydantic.BaseModel):
    """Represent a batch of `EntryCommand`s."""

    commands: Iterable[EntryCommand]
