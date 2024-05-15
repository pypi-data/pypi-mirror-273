# pylint: skip-file
__all__: Final[tuple[str, ...]] = (
    "linear_search",
    "depth_first_search",
    "breadth_first_search",
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "preorder",
    "inorder",
    "postorder",
    "levelorder",
    "reverse_inorder",
)

from typing import Final, TypeVar, overload

from nrw.datastructures import (
    BinarySearchTree,
    BinaryTree,
    ComparableContentT,
    Graph,
    List,
    Vertex,
)

_T = TypeVar("_T")

def linear_search(lst: List[_T], element: _T) -> int: ...
def depth_first_search(graph: Graph, vertex: Vertex) -> List[Vertex]: ...
def breadth_first_search(graph: Graph, vertex: Vertex) -> List[Vertex]: ...
def bubble_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def selection_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def insertion_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def merge_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
def quick_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]: ...
@overload
def preorder(tree: BinaryTree[_T], *, reverse: bool = False) -> List[_T]: ...
@overload
def preorder(
    tree: BinarySearchTree[ComparableContentT],
    *,
    reverse: bool = False,
) -> List[ComparableContentT]: ...
@overload
def inorder(tree: BinaryTree[_T], *, reverse: bool = False) -> List[_T]: ...
@overload
def inorder(
    tree: BinarySearchTree[ComparableContentT],
    *,
    reverse: bool = False,
) -> List[ComparableContentT]: ...
@overload
def reverse_inorder(tree: BinaryTree[_T]) -> List[_T]: ...
@overload
def reverse_inorder(
    tree: BinarySearchTree[ComparableContentT],
) -> List[ComparableContentT]: ...
@overload
def postorder(tree: BinaryTree[_T], *, reverse: bool = False) -> List[_T]: ...
@overload
def postorder(
    tree: BinarySearchTree[ComparableContentT],
    *,
    reverse: bool = False,
) -> List[ComparableContentT]: ...
@overload
def levelorder(tree: BinaryTree[_T], *, reverse: bool = False) -> List[_T]: ...
@overload
def levelorder(
    tree: BinarySearchTree[ComparableContentT],
    *,
    reverse: bool = False,
) -> List[ComparableContentT]: ...
