"""Sortieralgorithmen für `List[ComparableContentT]`."""

from __future__ import annotations

__all__: Final[tuple[str, ...]] = (
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
)

from typing import TYPE_CHECKING, Final

from nrw.datastructures._list import List

if TYPE_CHECKING:
    from nrw.datastructures._comparable_content import ComparableContentT


def bubble_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]:
    swapped: bool = True
    while swapped:
        swapped = False
        lst.to_first()
        while lst.has_access and lst._current.next_node is not None:
            if lst._current.content > lst._current.next_node.content:
                lst._current.content, lst._current.next_node.content = (
                    lst._current.next_node.content,
                    lst._current.content,
                )
                swapped = True
            lst.next()
    return lst


def selection_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]:
    result: List[ComparableContentT] = List()
    while not lst.is_empty:
        min_element: ComparableContentT = _get_min_element(lst)
        _delete(min_element, lst)
        result.append(min_element)
    return result


def _get_min_element(lst: List[ComparableContentT]) -> ComparableContentT:
    lst.to_first()
    min_element: ComparableContentT | None = lst.content
    assert min_element is not None
    lst.next()
    while lst.has_access:
        assert lst.content is not None
        min_element = min(min_element, lst.content)
        lst.next()
    return min_element


def _delete(element: ComparableContentT, lst: List[ComparableContentT]) -> None:
    lst.to_first()
    while lst.has_access:  # pragma: no branch
        if lst.content is element:
            lst.remove()
            return
        lst.next()


def insertion_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]:
    result: List[ComparableContentT] = List()
    lst.to_first()
    while lst.has_access:
        _insort(result, lst.content)  # type: ignore[misc]
        lst.next()
    return result


def _insort(lst: List[ComparableContentT], element: ComparableContentT) -> None:
    lst.to_first()
    while lst.has_access:
        if element < lst.content:
            lst.insert(element)
            return
        lst.next()
    lst.append(element)


def merge_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]:
    lst.to_first()
    lst.next()
    if not lst.has_access:
        return lst

    left: List[ComparableContentT] = List()
    right: List[ComparableContentT] = List()

    to_the_left: bool = True
    lst.to_first()
    while lst.has_access:
        if to_the_left:
            left.append(lst.content)
            to_the_left = False
        else:
            right.append(lst.content)
            to_the_left = True
        lst.next()

    return _merge(merge_sort(left), merge_sort(right))


def _merge(
    lst1: List[ComparableContentT],
    lst2: List[ComparableContentT],
) -> List[ComparableContentT]:
    if lst1.is_empty:  # pragma: no branch
        return lst2  # pragma: no cover
    if lst2.is_empty:  # pragma: no branch
        return lst1  # pragma: no cover

    result: List[ComparableContentT] = List()

    lst1.to_first()
    lst2.to_first()
    while lst1.has_access and lst2.has_access:
        if lst1.content < lst2.content:  # type: ignore[operator]
            result.append(lst1.content)
            lst1.next()
        else:
            result.append(lst2.content)
            lst2.next()

    while lst1.has_access:
        result.append(lst1.content)
        lst1.next()

    while lst2.has_access:
        result.append(lst2.content)
        lst2.next()

    return result


def quick_sort(lst: List[ComparableContentT]) -> List[ComparableContentT]:
    result: List[ComparableContentT] = List()

    if lst.is_empty:
        return result

    lst.to_first()
    pivot: ComparableContentT | None = lst.content
    assert pivot is not None
    lst.next()

    right: List[ComparableContentT] = List()
    left: List[ComparableContentT] = List()

    while lst.has_access:
        element: ComparableContentT | None = lst.content
        assert element is not None
        if element < pivot:
            left.append(element)
        else:
            right.append(element)
        lst.next()

    result.concat(quick_sort(left))
    result.append(pivot)
    result.concat(quick_sort(right))

    return result
