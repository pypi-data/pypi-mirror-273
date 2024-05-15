"""Implementation der generischen Klasse `List[_T]`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("List",)

from io import StringIO
from typing import Final, Generic, TypeVar

_T = TypeVar("_T")


class _ListNode(Generic[_T]):
    __slots__: Final[tuple[str, str]] = ("_content", "_next_node")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, content: _T) -> None:
        """Ein neues Objekt vom Typ `_ListNode[_T]` wird erschaffen.
        Der Inhalt wird per Parameter gesetzt. Der Verweis ist leer.
        """
        self._content: _T = content
        self._next_node: _ListNode[_T] | None = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(content={self._content!r}, "
            f"next_node={self._next_node!r})"
        )

    @property
    def content(self) -> _T:
        """Liefert das Inhaltsobjekt des Knotens."""
        return self._content

    @content.setter
    def content(self, new_content: _T) -> None:
        self._content = new_content

    @property
    def next_node(self) -> _ListNode[_T] | None:
        """Liefert das nächste Element des aktuellen Knotens."""
        return self._next_node

    @next_node.setter
    def next_node(self, new_next_node: _ListNode[_T] | None) -> None:
        self._next_node = new_next_node


class List(Generic[_T]):
    """Objekt der generischen Klasse `List` verwalten beliebig viele linear
    angeordnete Objekte. Auf höchstens ein Listenobjekt,
    aktuellesObjekt genannt, kann jeweils zugegriffen werden.
    Wenn eine Liste leer ist, vollständig durchlaufen wurde oder das aktuelle
    Objekt am Ende der Liste gelöscht wurde, gibt es kein aktuelles
    Objekt.

    Das erste oder das letzte Objekt einer Liste können durch einen Auftrag zum
    aktuellen Objekt gemacht werden. Außerdem kann das dem aktuellen Objekt
    folgende Listenobjekt zum neuen aktuellen Objekt werden.
    Das aktuelle Objekt kann gelesen, verändert oder gelöscht werden. Außerdem
    kann vor dem aktuellen Objekt ein Listenobjekt eingefügt werden.
    """

    __slots__: Final[tuple[str, str, str]] = ("_first", "_last", "_current")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None:
        """Eine leere Liste wird erzeugt."""
        self._first: _ListNode[_T] | None = None
        self._last: _ListNode[_T] | None = None
        self._current: _ListNode[_T] | None = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(first={self._first!r}, last={self._last!r}, "
            f"current={self._current!r})"
        )

    def __str__(self) -> str:
        if self.is_empty:
            return f"{self.__class__.__name__}()"

        with StringIO() as buffer:
            buffer.write(f"{self.__class__.__name__}(")
            temp: _ListNode[_T] | None = self._first
            while temp is not self._last:
                buffer.write(f"{temp.content} -> ")
                temp = temp.next_node
            buffer.write(f"{temp.content})")
            return buffer.getvalue()

    @property
    def is_empty(self) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn die Liste keine Objekte enthält,
        sonst liefert sie den Wert `False`.
        """
        return self._first is None

    @property
    def has_access(self) -> bool:
        """Die Anfrage liefert den Wert `True`, wenn es ein aktuelles Objekt gibt,
        sonst liefert sie den Wert `False`.
        """
        return self._current is not None

    def next(self) -> None:
        """Falls die Liste nicht leer ist, es ein aktuelles Objekt gibt und dieses
        nicht das letzte Objekt der Liste ist, wird das dem aktuellen Objekt in
        der Liste folgende Objekt zum aktuellen Objekt, andernfalls gibt es nach
        Ausführung des Auftrags kein aktuelles Objekt, d.h. `has_access` liefert
        den Wert `False`.
        """
        if not self.has_access:
            return
        self._current = self._current.next_node

    def to_first(self) -> None:
        """Falls die Liste nicht leer ist, wird das erste Objekt der Liste aktuelles
        Objekt. Ist die Liste leer, geschieht nichts.
        """
        if self.is_empty:
            return
        self._current = self._first

    def to_last(self) -> None:
        """Falls die Liste nicht leer ist, wird das letzte Objekt der Liste
        aktuelles Objekt. Ist die Liste leer, geschieht nichts.
        """
        if self.is_empty:
            return
        self._current = self._last

    @property
    def content(self) -> _T | None:
        """Falls es ein aktuelles Objekt gibt (`has_access is True`), wird das
        aktuelle Objekt zurückgegeben, andernfalls (`has_access is False`) gibt
        die Anfrage den Wert `None` zurück.
        """
        return self._current.content if self.has_access else None

    @content.setter
    def content(self, new_content: _T | None) -> None:
        if new_content is None or not self.has_access:
            return
        self._current.content = new_content

    def insert(self, content: _T | None) -> None:
        """Falls es ein aktuelles Objekt gibt (`has_access is True`), wird ein neues
        Objekt vor dem aktuellen Objekt in die Liste eingefügt. Das aktuelle
        Objekt bleibt unverändert.

        Wenn die Liste leer ist, wird `content` in die Liste eingefügt und es
        gibt weiterhin kein aktuelles Objekt (`has_access is False`).

        Falls es kein aktuelles Objekt gibt (`has_access is False`) und die Liste
        nicht leer ist oder `content` `None` ist, geschieht nichts.
        """
        if content is None:
            return

        new_node: _ListNode[_T] = _ListNode(content)
        if self.has_access:
            if self._current is not self._first:
                previous: _ListNode[_T] | None = self._get_previous(
                    self._current,
                )
                assert previous is not None
                new_node.next_node, previous.next_node = previous.next_node, new_node
            else:
                new_node.next_node, self._first = self._first, new_node
        elif self.is_empty:
            self._first = self._last = new_node

    def append(self, content: _T | None) -> None:
        """Falls `content` `None` ist, geschieht nichts.

        Ansonsten wird ein neues Objekt `content` am Ende der Liste eingefügt.
        Das aktuelle Objekt bleibt unverändert.

        Wenn die Liste leer ist, wird das Objekt `content` in die Liste eingefügt
        und es gibt weiterhin kein aktuelles Objekt (`has_access is False`).
        """
        if content is None:
            return

        new_node: _ListNode[_T] = _ListNode(content)
        if self.is_empty:
            self._first = self._last = new_node
        else:
            self._last.next_node = self._last = new_node

    def concat(self, other_list: List[_T] | None) -> None:
        """Falls es sich bei der Liste und `other_list` um dasselbe Objekt handelt,
        `other_list` `None` oder eine leere Liste ist, geschieht nichts.

        Ansonsten wird die Liste `other_list` an die aktuelle Liste angehängt.
        Anschliessend wird `other_list` eine leere Liste. Das aktuelle Objekt bleibt
        unverändert. Insbesondere bleibt `has_access` identisch.
        """
        if other_list is self or other_list is None or other_list.is_empty:
            return

        if self.is_empty:
            self._first, self._last = other_list._first, other_list._last
        else:
            self._last.next_node, self._last = other_list._first, other_list._last

        other_list._first = other_list._last = other_list._current = None

    def remove(self) -> None:
        """Wenn die Liste leer ist oder es kein aktuelles Objekt gibt (`has_access
        is False`), geschieht nichts.

        Falls es ein aktuelles Objekt gibt (`has_access is True`), wird das
        aktuelle Objekt gelöscht und das Objekt hinter dem gelöschten Objekt
        wird zum aktuellen Objekt.

        Wird das Objekt, das am Ende der Liste steht, gelöscht, gibt es kein
        aktuelles Objekt mehr.
        """
        if not self.has_access or self.is_empty:
            return

        if self._current is self._first:
            self._first = self._first.next_node
        else:
            previous: _ListNode[_T] | None = self._get_previous(self._current)
            assert previous is not None
            if self._current is self._last:
                self._last = previous
            previous.next_node = self._current.next_node

        self._current = self._current.next_node

        if self.is_empty:
            self._last = None

    def _get_previous(self, node: _ListNode[_T] | None) -> _ListNode[_T] | None:
        """Liefert den Vorgängerknoten des Knotens `node`. Ist die Liste leer, `node
        is None`, `node` nicht in der Liste oder `node` der erste Knoten der Liste,
        wird `None` zurückgegeben.
        """
        if node is None or node == self._first or self.is_empty:
            return None

        temp: _ListNode[_T] | None = self._first
        while temp is not None and temp.next_node is not node:
            temp = temp.next_node
        return temp
