"""Suchalgorithmen für `List[ComparableContentT]`."""

from __future__ import annotations

__all__: Final[tuple[str, ...]] = (
    "linear_search",
    "depth_first_search",
    "breadth_first_search",
)

from typing import TYPE_CHECKING, Final, TypeVar

from nrw.datastructures._list import List

if TYPE_CHECKING:
    from nrw.datastructures._edge import Edge
    from nrw.datastructures._graph import Graph
    from nrw.datastructures._vertex import Vertex

_T = TypeVar("_T")


def linear_search(lst: List[_T], element: _T) -> int:
    lst.to_first()
    index: int = 0
    while lst.has_access:
        if lst.content == element:
            return index
        index += 1
        lst.next()
    return index


def _depth_first_search_impl(graph: Graph, vertex: Vertex) -> List[Vertex]:
    assert graph.get_vertex(vertex.id) is not None
    result: List[Vertex] = List()

    if vertex.is_marked:
        return result

    result.append(vertex)
    vertex.mark = True

    neighbours: List[Vertex] = graph.get_neighbours(vertex)
    neighbours.to_first()
    while neighbours.has_access:
        current: Vertex | None = neighbours.content
        assert current is not None
        result.concat(_depth_first_search_impl(graph, current))
        neighbours.next()

    return result


def depth_first_search(graph: Graph, vertex: Vertex) -> List[Vertex]:
    if graph.is_empty or graph.get_vertex(vertex.id) is None:
        return List()

    graph.set_all_vertex_marks(False)
    graph.set_all_edge_marks(False)
    return _depth_first_search_impl(graph, vertex)


def breadth_first_search(graph: Graph, vertex: Vertex) -> List[Vertex]:
    result: List[Vertex] = List()

    if graph.is_empty or graph.get_vertex(vertex.id) is None:
        return result

    graph.set_all_vertex_marks(False)
    graph.set_all_edge_marks(False)

    vertex.mark = True
    result.append(vertex)

    result.to_first()
    while result.has_access:
        current: Vertex | None = result.content
        assert current is not None
        neighbours: List[Vertex] = graph.get_neighbours(current)
        neighbours.to_first()
        while neighbours.has_access:
            current_neighbour: Vertex | None = neighbours.content
            assert current_neighbour is not None
            if not current_neighbour.is_marked:
                edge: Edge | None = graph.get_edge(current_neighbour, current)
                assert edge is not None
                edge.mark = True
                current_neighbour.mark = True
                result.append(current_neighbour)
            neighbours.next()
        result.next()

    return result
