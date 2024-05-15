"""Implementation der Klasse `Edge`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("Edge",)

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from nrw.datastructures._vertex import Vertex


class Edge:
    """Die Klasse `Edge` stellt eine einzelne, ungerichtete Kante eines Graphen dar.
    Beim Erstellen werden die beiden durch sie zu verbindenden Knotenobjekte und eine
    Gewichtung als `int` übergeben. Beide Knotenobjekte können abgefragt werden.
    Des Weiteren koennen die Gewichtung
    und eine Markierung gesetzt und abgefragt werden.
    """

    __slots__: Final[tuple[str, str, str]] = ("_vertices", "_weight", "_mark")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, vertex: Vertex, another_vertex: Vertex, weight: int) -> None:
        """Ein neues Objekt vom Typ `Edge` wird erstellt. Die von diesem Objekt
        repraesentierte Kante verbindet die Knoten `vertex` und `another_vertex` mit der
        Gewichtung `weight`. Ihre Markierung hat den Wert `False`.
        """
        self._vertices: tuple[Vertex, Vertex] = (vertex, another_vertex)
        self._weight: int = weight
        self._mark: bool = False

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(vertices={self._vertices!r}, "
            f"weight={self._weight!r}, mark={self._mark!r})"
        )

    def __str__(self) -> str:
        vertex1, vertex2 = self._vertices
        return f"{vertex1} --{self._weight}-- {vertex2}"

    @property
    def vertices(self) -> tuple[Vertex, Vertex]:
        """Die Anfrage gibt die beiden Knoten, die durch die Kante verbunden werden,
        als `tuple` vom Typ `Vertex` zurück.
        Das `tuple` hat genau zwei Einträge mit den Indexwerten 0 und 1.
        """
        return self._vertices

    @property
    def weight(self) -> int:
        """Der Auftrag setzt das Gewicht der Kante auf `weight`."""
        return self._weight

    @weight.setter
    def weight(self, new_weight: int) -> None:
        self._weight = new_weight

    @property
    def mark(self) -> bool:
        """Die Anfrage liefert `True`,
        wenn die Markierung der Kante den Wert `True` hat, ansonsten `False`.
        """
        return self._mark

    @mark.setter
    def mark(self, new_mark: bool) -> None:
        self._mark = new_mark

    @property
    def is_marked(self) -> bool:
        """Die Anfrage liefert `True`,
        wenn die Markierung der Kante den Wert `True` hat, ansonsten `False`.
        """
        return self._mark
