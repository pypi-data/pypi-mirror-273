"""Implementation der generischen Klasse `BinarySearchTree[ComparableContentT]`."""

from __future__ import annotations

from typing import Final, Generic

from nrw.datastructures._comparable_content import ComparableContentT
from nrw.datastructures._utils import display_binary_node


class _BSTNode(Generic[ComparableContentT]):
    """Durch diese innere Klasse kann man dafür sorgen, dass ein leerer Baum
    `None` ist, ein nicht-leerer Baum jedoch immer eine nicht-`None`-Wurzel sowie
    nicht-`None`-Teilbäume hat.
    """

    __slots__: Final[tuple[str, str, str]] = ("_content", "_left", "_right")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, content: ComparableContentT) -> None:
        self._content: ComparableContentT = content
        self._left: BinarySearchTree[ComparableContentT] = BinarySearchTree()
        self._right: BinarySearchTree[ComparableContentT] = BinarySearchTree()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(content={self._content!r}, "
            f"left_tree={self._left!r}, right_tree={self._right!r})"
        )

    def __str__(self) -> str:
        return display_binary_node(self)


class BinarySearchTree(Generic[ComparableContentT]):
    """Mithilfe der generischen Klasse `BinarySearchTree` können beliebig viele
    Objekte in einem Binaerbaum (binaerer Suchbaum) entsprechend einer
    Ordnungsrelation verwaltet werden.

    Ein Objekt der Klasse stellt entweder einen leeren binären Suchbaum dar oder
    verwaltet ein Inhaltsobjekt sowie einen linken und einen rechten Teilbaum,
    die ebenfalls Objekte der Klasse `BinarySearchTree` sind.

    Die Klasse der Objekte, die in dem Suchbaum verwaltet werden sollen, muss
    das Protocol `ComparableContent` implementieren. Dabei muss durch
    Ueberschreiben der drei Vergleichsmethoden `__lt__`, `__eq__`, `__gt__` (s.
    Dokumentation des Protocols) eine eindeutige Ordnungsrelation festgelegt
    sein.

    Alle Objekte im linken Teilbaum sind kleiner als das Inhaltsobjekt des
    binären Suchbaums. Alle Objekte im rechten Teilbaum sind grösser als das
    Inhaltsobjekt des binären Suchbaums. Diese Bedingung gilt (rekursiv) auch in
    beiden Teilbäumen.

    Hinweis: In dieser Version wird die Klasse `BinaryTree` nicht benutzt.
    """

    __slots__: Final[tuple[str]] = ("_node",)
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None:
        """Der Konstruktor erzeugt einen leeren Suchbaum."""
        self._node: _BSTNode[ComparableContentT] | None = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(node={self._node!r})"

    def __str__(self) -> str:
        return str(self._node) if not self.is_empty else ""

    @property
    def is_empty(self) -> bool:
        """Diese Anfrage liefert den Wahrheitswert `True`, wenn der Suchbaum leer ist,
        sonst liefert sie den Wert `False`.
        """
        return self._node is None

    @property
    def content(self) -> ComparableContentT | None:
        """Diese Anfrage liefert das Inhaltsobjekt des Suchbaumes. Wenn der Suchbaum
        leer ist, wird `None` zurückgegeben.
        """
        return self._node._content if not self.is_empty else None

    @property
    def left_tree(self) -> BinarySearchTree[ComparableContentT] | None:
        """Diese Anfrage liefert den linken Teilbaum des binären Suchbaumes.

        Wenn er leer ist, wird `None` zurückgegeben.
        """
        return self._node._left if not self.is_empty else None

    @property
    def right_tree(self) -> BinarySearchTree[ComparableContentT] | None:
        """Diese Anfrage liefert den rechten Teilbaum des binären Suchbaumes.

        Wenn er leer ist, wird `None` zurückgegeben.
        """
        return self._node._right if not self.is_empty else None

    def insert(self, content: ComparableContentT | None) -> None:
        """Falls der Parameter `None` ist, geschieht nichts.

        Falls ein bezüglich des verwendeten Vergleichs `==` mit
        `content` übereinstimmendes Objekt im geordneten binaeren Suchbau
        enthalten ist, passiert nichts.

        Achtung: hier wird davon ausgegangen, dass `==` genau dann `True`
        liefert, wenn `<` und `>` `False` liefern.

        Andernfalls (`<` order `>`) wird das Objekt `content` entsprechend
        der vorgegebenen Ordnungsrelation in den `BinarySearchTree` eingeordnet.
        """
        if content is None:
            return

        if self.is_empty:
            self._node = _BSTNode(content)
        elif content < self._node._content:
            self._node._left.insert(content)
        elif content > self._node._content:
            self._node._right.insert(content)

    def remove(self, content: ComparableContentT | None) -> None:
        """Falls ein bezüglich des verwendeten Vergleichs mit
        `content` übereinstimmendes Objekt im binaeren Suchbaum enthalten
        ist, wird dieses entfernt. Falls der Parameter `None` ist, ändert sich
        nichts.
        """
        if self.is_empty or content is None:
            return

        if content < self._node._content:
            self._node._left.remove(content)
        elif content > self._node._content:
            self._node._right.remove(content)
        elif self._node._left.is_empty and self._node._right.is_empty:
            self._node = None
        elif self._node._left.is_empty and not self._node._right.is_empty:
            self._node = self._node_of_right_successor
        elif not self._node._left.is_empty and self._node._right.is_empty:
            self._node = self._node_of_left_successor
        elif self._node_of_right_successor._left.is_empty:
            self._node._content, self._node._right = (
                self._node_of_right_successor._content,
                self._node_of_right_successor._right,
            )
        else:
            previous: BinarySearchTree[ComparableContentT] = (
                self._node._right._ancestor_of_small_right()
            )
            smallest: BinarySearchTree[ComparableContentT] | None = previous._node._left
            self._node._content = smallest._node._content
            previous.remove(smallest._node._content)

    def search(self, content: ComparableContentT | None) -> ComparableContentT | None:
        """Falls ein bezüglich des verwendeten Vergleichs `==` mit
        `content` übereinstimmendes Objekt im binaeren Suchbaum enthalten ist,
        liefert die Anfrage dieses, ansonsten wird `None` zurückgegeben.

        Falls der Parameter `None` ist, wird `None` zurückgegeben.
        """
        if self.is_empty or content is None:
            return None

        if content < self._node._content:
            return self.left_tree.search(content)
        if content > self._node._content:
            return self.right_tree.search(content)
        if content == self._node._content:
            return self._node._content
        return None  # pragma: no cover

    def _ancestor_of_small_right(self) -> BinarySearchTree[ComparableContentT]:
        """Die Methode liefert denjenigen Baum, dessen linker Nachfolger keinen linken
        Nachfolger mehr hat. Es ist also später möglich, in einem Baum im
        rechten Nachfolger den Vorgänger des linkesten Nachfolgers zu finden.
        """
        if self._node_of_left_successor._left.is_empty:
            return self
        return self._node._left._ancestor_of_small_right()

    @property
    def _node_of_left_successor(self) -> _BSTNode[ComparableContentT] | None:
        return self._node._left._node

    @property
    def _node_of_right_successor(self) -> _BSTNode[ComparableContentT] | None:
        return self._node._right._node
