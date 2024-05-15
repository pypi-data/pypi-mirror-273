"""Klasse `QueryResult`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("QueryResult",)

from typing import Any, Final


class QueryResult:
    """Ein Objekt der Klasse `QueryResult` stellt die Ergebnistabelle einer
    Datenbankanfrage mit Hilfe
    der Klasse `DatabaseConnector` dar. Objekte dieser Klasse werden nur von der
    Klasse `DatabaseConnector` erstellt.
    Die Klasse verfügt über keinen öffentlichen Konstruktor.
    """

    __slots__: Final[tuple[str, str, str]] = ("_data", "_column_names", "_column_types")

    def __init__(
        self,
        data: list[tuple[Any, ...]],
        column_names: tuple[str, ...],
        column_types: tuple[type | str | None, ...],
    ) -> None:
        """Interner Konstruktor."""
        self._data: list[tuple[Any, ...]] = data
        self._column_names: tuple[str, ...] = column_names
        self._column_types: tuple[type | str | None, ...] = column_types

    @property
    def data(self) -> list[tuple[Any, ...]]:
        """Die Anfrage liefert die Einträge der Ergebnistabelle als eine `list`
        welche wiederum `tuple` enthält. Der erste Index stellt die Zeile und der zweite
        die Spalte dar (d.h. Object[zeile][spalte]).
        """
        return self._data

    @property
    def column_names(self) -> tuple[str, ...]:
        """Die Anfrage liefert die Bezeichner der Spalten der Ergebnistabelle als
        `tuple` vom Typ `str` zurück.
        """
        return self._column_names

    @property
    def column_types(self) -> tuple[type | str | None, ...]:
        """Die Anfrage liefert (wenn möglich) die Typenbezeichnung der Spalten der
        Ergebnistabelle als `tuple` vom jeweiligen Typ zurück.
        Die Bezeichnungen entsprechen den Angaben in der `MySQL`-Datenbank.
        """
        return self._column_types

    @property
    def row_count(self) -> int:
        """Die Anfrage liefert die Anzahl der Zeilen der Ergebnistabelle als `int`."""
        return len(self._data) if self._data is not None else 0

    @property
    def column_count(self) -> int:
        """Die Anfrage liefert die Anzahl der Spalten der Ergebnistabelle als `int`."""
        assert all(len(self._data[0]) == len(data) for data in self._data[1:])
        return len(self._data[0])
