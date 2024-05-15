"""Implementation der Klasse `Vertex`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("Vertex",)

from typing import Final


class Vertex:
    """Die Klasse Vertex stellt einen einzelnen Knoten eines Graphen dar. Jedes Objekt
    dieser Klasse verfügt über eine im Graphen eindeutige ID als String und kann diese
    ID zurückliefern.
    Darüber hinaus kann eine Markierung gesetzt und abgefragt werden.
    """

    __slots__: Final[tuple[str, str]] = ("_id", "_mark")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, id_: str) -> None:
        """Ein neues Objekt vom Typ `Vertex` wird erstellt.
        Seine Markierung hat den Wert `False`.
        """
        self._id: str = id_
        self._mark: bool = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id!r}, mark={self._mark!r})"

    def __str__(self) -> str:
        return self._id

    @property
    def id(self) -> str:
        """Die Anfrage liefert die ID des Knotens als String."""
        return self._id

    @property
    def mark(self) -> bool:
        """Die Anfrage liefert `True`,
        wenn die Markierung des Knotens den Wert `True` hat, ansonsten `False`.
        """
        return self._mark

    @mark.setter
    def mark(self, new_mark: bool) -> None:
        self._mark = new_mark

    @property
    def is_marked(self) -> bool:
        """Die Anfrage liefert `True`,
        wenn die Markierung des Knotens den Wert `True` hat, ansonsten `False`.
        """
        return self._mark
