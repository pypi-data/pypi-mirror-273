from __future__ import annotations

__all__: Final[tuple[str, ...]] = ("display_binary_node",)

from typing import TYPE_CHECKING, Final, TypeVar

if TYPE_CHECKING:
    from nrw.datastructures._binary_search_tree import _BSTNode
    from nrw.datastructures._binary_tree import _BTNode
    from nrw.datastructures._comparable_content import ComparableContentT

_T = TypeVar("_T")


def display_binary_node(node: _BTNode[_T] | _BSTNode[ComparableContentT]) -> str:
    lines, *_ = _display_binary_node_impl(node)
    return "\n".join(lines)


def _display_binary_node_impl(  # pylint: disable=R0914
    node: _BTNode[_T] | _BSTNode[ComparableContentT],
) -> tuple[list[str], int, int, int]:
    """Based on the implementation by J.V.

    https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python/54074933#54074933
    """
    if (node._right is None or node._right.is_empty) and (
        node._left is None or node._left.is_empty
    ):
        line: str = str(node._content)
        width: int = len(line)
        height: int = 1
        middle: int = width // 2
        return [line], width, height, middle

    content: str
    content_len: int
    first_line: str
    second_line: str
    shifted_lines: list[str]
    if (node._right is None or node._right.is_empty) and not node._left.is_empty:
        assert node._left._node is not None
        lines, n, p, x = _display_binary_node_impl(node._left._node)
        content = str(node._content)
        content_len = len(content)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + content
        second_line = x * " " + "/" + (n - x - 1 + content_len) * " "
        shifted_lines = [line + content_len * " " for line in lines]
        return (
            [first_line, second_line, *shifted_lines],
            n + content_len,
            p + 2,
            n + content_len // 2,
        )

    if (node._left is None or node._left.is_empty) and not node._right.is_empty:
        assert node._right._node is not None
        lines, n, p, x = _display_binary_node_impl(node._right._node)
        content = str(node._content)
        content_len = len(content)
        first_line = content + x * "_" + (n - x) * " "
        second_line = (content_len + x) * " " + "\\" + (n - x - 1) * " "
        shifted_lines = [content_len * " " + line for line in lines]
        return (
            [first_line, second_line, *shifted_lines],
            n + content_len,
            p + 2,
            content_len // 2,
        )

    assert node._left._node is not None
    assert node._right._node is not None
    left, n, p, x = _display_binary_node_impl(node._left._node)
    right, m, q, y = _display_binary_node_impl(node._right._node)
    content = str(node._content)
    content_len = len(content)
    first_line = (x + 1) * " " + (n - x - 1) * "_" + content + y * "_" + (m - y) * " "
    second_line = (
        x * " " + "/" + (n - x - 1 + content_len + y) * " " + "\\" + (m - y - 1) * " "
    )
    if p < q:  # pragma: no cover
        left += [n * " "] * (q - p)
    elif q < p:  # pragma: no cover
        right += [m * " "] * (p - q)
    zipped_lines = zip(left, right)
    lines = [first_line, second_line] + [
        a + content_len * " " + b for a, b in zipped_lines
    ]
    return lines, n + m + content_len, max(p, q) + 2, n + content_len // 2
