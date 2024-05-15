# pylint: skip-file
__all__: Final[tuple[str]] = ("QueryResult",)

from typing import Any, Final

class QueryResult:
    __slots__: Final[tuple[str, str, str]] = ("_data", "_column_names", "_column_types")
    def __init__(
        self,
        data: list[tuple[Any, ...]],
        column_names: tuple[str, ...],
        column_types: tuple[type | str | None, ...],
    ) -> None: ...
    @property
    def data(self) -> list[tuple[Any, ...]]: ...
    @property
    def column_names(self) -> tuple[str, ...]: ...
    @property
    def column_types(self) -> tuple[type | str | None, ...]: ...
    @property
    def row_count(self) -> int: ...
    @property
    def column_count(self) -> int: ...
