"""Implementation der generischen Klasse `Stack[_T]`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("Stack",)

from io import StringIO
from typing import Final, Generic, TypeVar

_T = TypeVar("_T")


class _StackNode(Generic[_T]):
    __slots__: Final[tuple[str, str]] = ("_content", "_next_node")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, content: _T) -> None:
        """Ein neues Objekt vom Typ `_StackNode[_T]` wird erschaffen.
        Der Inhalt wird per Parameter gesetzt. Der Verweis ist leer.
        """
        self._content: _T = content
        self._next_node: _StackNode[_T] | None = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(content={self._content!r}, "
            f"next_node={self._next_node!r})"
        )

    @property
    def content(self) -> _T:
        """Liefert das Inhaltsobjekt des Knotens."""
        return self._content

    @property
    def next_node(self) -> _StackNode[_T] | None:
        """Liefert das nächste Element des aktuellen Knotens."""
        return self._next_node

    @next_node.setter
    def next_node(self, new_next_node: _StackNode[_T] | None) -> None:
        self._next_node = new_next_node


class Stack(Generic[_T]):
    """Objekte der generischen Klasse `Stack` (Keller, Stapel) verwalten beliebige
    Objekte nach dem Last-In-First-Out-Prinzip, d.h., das
    zuletzt abgelegte Objekt wird als erstes wieder entnommen. Alle Methoden
    haben eine konstante Laufzeit, unabhängig von der Anzahl der verwalteten
    Objekte.
    """

    __slots__: Final[tuple[str]] = ("_head",)
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None:
        """Ein leerer Stapel wird erzeugt."""
        self._head: _StackNode[_T] | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(head={self._head!r})"

    def __str__(self) -> str:
        if self.is_empty:
            return f"{self.__class__.__name__}()"

        with StringIO() as buffer:
            buffer.write(f"{self.__class__.__name__}(")
            temp: _StackNode[_T] | None = self._head
            while temp is not None and temp.next_node is not None:
                buffer.write(f"{temp.content} -> ")
                temp = temp.next_node
            buffer.write(f"{temp.content})")
            return buffer.getvalue()

    @property
    def is_empty(self) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn der Stapel keine Objekte enthält,
        sonst liefert sie den Wert `False`.
        """
        return self._head is None

    def push(self, content: _T) -> None:
        """Das Objekt `content` wird oben auf den Stapel gelegt.
        Falls `content` `None` ist, bleibt der Stapel unverändert.
        """
        if content is None:
            return

        new_node: _StackNode[_T] = _StackNode(content)
        new_node.next_node, self._head = self._head, new_node

    def pop(self) -> None:
        """Das zuletzt eingefügte Objekt wird von dem Stapel entfernt.
        Falls der Stapel leer ist, bleibt er unverändert.
        """
        if self.is_empty:
            return
        self._head = self._head.next_node

    @property
    def top(self) -> _T | None:
        """Die Anfrage liefert das oberste Stapelobjekt. Der Stapel bleibt unverändert.
        Falls der Stapel leer ist, wird `None` zurückgegeben.
        """
        return self._head.content if not self.is_empty else None
