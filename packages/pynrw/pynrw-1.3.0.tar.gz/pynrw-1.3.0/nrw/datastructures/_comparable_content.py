"""Implementation des generischen Protocols `ComparableContent[_T_contra]`."""

from __future__ import annotations

__all__: Final[tuple[str, str]] = ("ComparableContent", "ComparableContentT")

from typing import Any, Final, Protocol, TypeVar, runtime_checkable

_T_contra = TypeVar("_T_contra", contravariant=True)


@runtime_checkable
class ComparableContent(Protocol[_T_contra]):
    """Das generische Protocol `ComparableContent[_T_contra]` legt die Methoden
    fest, über die Objekte verfügen müssen, die in einen binaeren Suchbaum
    (`BinarySearchTree`) eingefügt werden sollen.
    """

    def __eq__(self, other: object, /) -> bool: ...
    def __gt__(self, other: _T_contra, /) -> bool: ...
    def __lt__(self, other: _T_contra, /) -> bool: ...


ComparableContentT = TypeVar("ComparableContentT", bound=ComparableContent[Any])
