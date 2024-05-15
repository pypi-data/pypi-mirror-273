"""Nützliche Algorithmen für die Datenstrukturen."""

from __future__ import annotations

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

from typing import Final

from nrw.algorithms._searching import (
    breadth_first_search,
    depth_first_search,
    linear_search,
)
from nrw.algorithms._sorting import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from nrw.algorithms._traversal import (
    inorder,
    levelorder,
    postorder,
    preorder,
    reverse_inorder,
)
