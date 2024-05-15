"""Implementation der generischen Klasse `Queue[_T]`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("Queue",)

from io import StringIO
from typing import Final, Generic, TypeVar

_T = TypeVar("_T")


class _QueueNode(Generic[_T]):
    __slots__: Final[tuple[str, str]] = ("_content", "_next_node")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, content: _T) -> None:
        """Ein neues Objekt vom Typ `_QueueNode[_T]` wird erschaffen.
        Der Inhalt wird per Parameter gesetzt. Der Verweis ist leer.
        """
        self._content: _T = content
        self._next_node: _QueueNode[_T] | None = None

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
    def next_node(self) -> _QueueNode[_T] | None:
        """Liefert das nächste Element des aktuellen Knotens."""
        return self._next_node

    @next_node.setter
    def next_node(self, new_next_node: _QueueNode[_T] | None) -> None:
        self._next_node = new_next_node


class Queue(Generic[_T]):
    """Objekte der generischen Klasse `Queue` (Warteschlange) verwalten beliebige
    Objekte nach dem First-In-First-Out-Prinzip, d.h., das
    zuerst abgelegte Objekt wird als erstes wieder entnommen. Alle Methoden haben
    eine konstante Laufzeit, unabhängig von der Anzahl der verwalteten Objekte.
    """

    __slots__: Final[tuple[str, str]] = ("_head", "_tail")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None:
        """Eine leere Schlange wird erzeugt."""
        self._head: _QueueNode[_T] | None = None
        self._tail: _QueueNode[_T] | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(head={self._head!r}, tail={self._tail!r})"

    def __str__(self) -> str:
        if self.is_empty:
            return f"{self.__class__.__name__}()"

        with StringIO() as buffer:
            buffer.write(f"{self.__class__.__name__}(")
            temp: _QueueNode[_T] | None = self._head
            while temp is not self._tail:
                buffer.write(f"{temp.content} -> ")
                temp = temp.next_node
            buffer.write(f"{temp.content})")
            return buffer.getvalue()

    @property
    def is_empty(self) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn die Schlange keine Objekte enthält,
        sonst liefert sie den Wert `False`.
        """
        return self._head is None

    def enqueue(self, content: _T) -> None:
        """Das Objekt `content` wird an die Schlange angehängt.
        Falls `content` `None` ist, bleibt die Schlange unverändert.
        """
        if content is None:
            return

        new_node: _QueueNode[_T] = _QueueNode(content)

        if self.is_empty:
            self._head = self._tail = new_node
        else:
            self._tail.next_node, self._tail = new_node, new_node

    def dequeue(self) -> None:
        """Das erste Objekt wird aus der Schlange entfernt.
        Falls die Schlange leer ist, wird sie nicht verändert.
        """
        if self.is_empty:
            return

        self._head = self._head.next_node

        if self.is_empty:
            self._head = self._tail = None

    @property
    def front(self) -> _T | None:
        """Die Anfrage liefert das erste Objekt der Schlange.
        Die Schlange bleibt unverändert.
        Falls die Schlange leer ist, wird `None` zurückgegeben.
        """
        return self._head.content if not self.is_empty else None
