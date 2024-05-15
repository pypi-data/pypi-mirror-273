"""Die Datenstrukturen nach den Vorgaben des Landes NRW."""

from __future__ import annotations

__all__: Final[tuple[str, ...]] = (
    "Stack",
    "Queue",
    "List",
    "BinaryTree",
    "ComparableContent",
    "ComparableContentT",
    "Vertex",
    "Edge",
    "BinarySearchTree",
    "Graph",
)

from typing import Final

from nrw.datastructures._binary_search_tree import BinarySearchTree
from nrw.datastructures._binary_tree import BinaryTree
from nrw.datastructures._comparable_content import ComparableContent, ComparableContentT
from nrw.datastructures._edge import Edge
from nrw.datastructures._graph import Graph
from nrw.datastructures._list import List
from nrw.datastructures._queue import Queue
from nrw.datastructures._stack import Stack
from nrw.datastructures._vertex import Vertex
