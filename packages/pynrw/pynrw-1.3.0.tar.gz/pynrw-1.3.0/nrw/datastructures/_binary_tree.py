"""Implementation der generischen Klasse `BinaryTree[_T]`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("BinaryTree",)

from typing import Final, Generic, TypeVar

from nrw.datastructures._utils import display_binary_node

_T = TypeVar("_T")


class _BTNode(Generic[_T]):
    """Durch diese innere Klasse kann man dafür sorgen, dass ein leerer Baum `None`
    ist, ein nicht-leerer Baum jedoch immer eine nicht-`None`-Wurzel sowie
    nicht-`None`-Teilbäume, ggf. leere Teilbäume hat.
    """

    __slots__: Final[tuple[str, str, str]] = ("_content", "_left", "_right")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self, content: _T) -> None:
        self._content: _T = content
        self._left: BinaryTree[_T] | None = BinaryTree()
        self._right: BinaryTree[_T] | None = BinaryTree()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(content={self._content!r}, "
            f"left_tree={self._left!r}, right_tree={self._right!r})"
        )

    def __str__(self) -> str:
        return display_binary_node(self)


class BinaryTree(Generic[_T]):
    """Mithilfe der generischen Klasse `BinaryTree` können beliebig viele
    Inhaltsobjekte in einem Binaerbaum verwaltet werden. Ein
    Objekt der Klasse stellt entweder einen leeren Baum dar oder verwaltet ein
    Inhaltsobjekt sowie einen linken und einen rechten Teilbaum, die ebenfalls
    Objekte der generischen Klasse `BinaryTree` sind.
    """

    __slots__: Final[tuple[str]] = ("_node",)
    __hash__ = None  # type: ignore[assignment]

    def __init__(
        self,
        content: _T | None = None,
        left_tree: BinaryTree[_T] | None = None,
        right_tree: BinaryTree[_T] | None = None,
    ) -> None:
        """Nach dem Aufruf des Konstruktors ohne Parameter existiert ein leerer
        Binaerbaum.

        Wenn der Parameter `content` gegeben und nicht `None` ist, existiert nach dem
        Aufruf des Konstruktors der Binaerbaum und hat `content` als Inhaltsobjekt
        und zwei leere Teilbäume.
        Falls der Parameter `None` ist, wird ein leerer Binaerbaum erzeugt.


        Wenn der Parameter `content` gegeben und nicht `None` ist
        sowie die Parameter `left_tree` und `right_tree` gegenben sind,
        wird ein Binaerbaum mit `content` als Inhalt und den beiden Teilbäumen
        `left_tree` und `right_tree` erzeugt.
        Sind `left_tree` und `right_tree` `None`, wird der entsprechende
        Teilbaum als leerer Binaerbaum eingefügt. So kann es also nie passieren,
        dass linke oder rechte Teilbäume `None` sind. Wenn der Parameter `content`
        `None` ist, wird ein leerer Binaerbaum erzeugt.
        """
        if content is None:
            self._node: _BTNode[_T] | None = None
        else:
            self._node = _BTNode(content)
            self._node._left = left_tree if left_tree is not None else BinaryTree()
            self._node._right = right_tree if right_tree is not None else BinaryTree()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(node={self._node!r})"

    def __str__(self) -> str:
        if self.is_empty:
            return ""
        return str(self._node)

    @property
    def is_empty(self) -> bool:
        """Diese Anfrage liefert das Inhaltsobjekt des Binaerbaums. Wenn der Binaerbaum
        leer ist, wird `None` zurueckgegeben.
        """
        return self._node is None

    @property
    def content(self) -> _T | None:
        """Diese Anfrage liefert das Inhaltsobjekt des Binaerbaums. Wenn der Binaerbaum
        leer ist, wird `None` zurückgegeben.
        """
        return self._node._content if not self.is_empty else None

    @content.setter
    def content(self, new_content: _T | None) -> None:
        if new_content is None:
            return

        if self.is_empty:
            self._node = _BTNode(new_content)
            self._node._left = BinaryTree()
            self._node._right = BinaryTree()
        else:
            self._node._content = new_content

    @property
    def left_tree(self) -> BinaryTree[_T] | None:
        """Diese Anfrage liefert den linken Teilbaum des Binaerbaumes. Wenn der
        Binaerbaum leer ist, wird `None` zurückgegeben.
        """
        return self._node._left if not self.is_empty else None

    @left_tree.setter
    def left_tree(self, new_tree: BinaryTree[_T] | None) -> None:
        if self.is_empty or new_tree is None:
            return
        self._node._left = new_tree

    @property
    def right_tree(self) -> BinaryTree[_T] | None:
        """Diese Anfrage liefert den rechten Teilbaum des Binaerbaumes. Wenn der
        Binaerbaum leer ist, wird `None` zurückgegeben.
        """
        return self._node._right if not self.is_empty else None

    @right_tree.setter
    def right_tree(self, new_tree: BinaryTree[_T] | None) -> None:
        if self.is_empty or new_tree is None:
            return
        self._node._right = new_tree
