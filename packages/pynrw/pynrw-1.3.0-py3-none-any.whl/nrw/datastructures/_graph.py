"""Implementation der Klasse `Graph`."""

from __future__ import annotations

__all__: Final[tuple[str]] = ("Graph",)

from io import StringIO
from typing import TYPE_CHECKING, Final

from nrw.datastructures._list import List

if TYPE_CHECKING:
    from nrw.datastructures._edge import Edge
    from nrw.datastructures._vertex import Vertex


class Graph:
    """Die Klasse `Graph` stellt einen ungerichteten, kantengewichteten Graphen dar.
    Es können Knoten- und Kantenobjekte hinzugefügt und entfernt,
    flache Kopien der Knoten- und Kantenlisten des Graphen angefragt
    und Markierungen von Knoten und Kanten gesetzt und überprueft werden.
    Des Weiteren kann eine Liste der Nachbarn eines bestimmten Knoten,
    eine Liste der inzidenten Kanten eines bestimmten Knoten
    und die Kante von einem bestimmten Knoten zu einem
    anderen bestimmten Knoten angefragt werden.
    Abgesehen davon kann abgefragt werden, welches
    Knotenobjekt zu einer bestimmten ID gehört und ob der Graph leer ist.
    """

    __slots__: Final[tuple[str, str]] = ("_vertices", "_edges")
    __hash__ = None  # type: ignore[assignment]

    def __init__(self) -> None:
        """Ein Objekt vom Typ `Graph` wird erstellt.
        Der von diesem Objekt repraesentierte Graph ist leer.
        """
        self._vertices: List[Vertex] = List()
        self._edges: List[Edge] = List()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(vertices={self._vertices!r}, "
            f"edges={self._edges!r})"
        )

    def __str__(self) -> str:
        if self.is_empty:
            return f"{self.__class__.__name__}()"

        with StringIO() as buffer:
            buffer.write(f"{self.__class__.__name__}(")
            self._vertices.to_first()
            while self._vertices.has_access:
                current: Vertex | None = self._vertices.content
                assert current is not None
                buffer.write(f"{current} -> {self.get_neighbours(current)}, ")
                self._vertices.next()
            return f"{buffer.getvalue().rstrip(', ')})"

    @property
    def vertices(self) -> List[Vertex]:
        """Die Anfrage liefert eine neue Liste aller Knotenobjekte
        vom Typ `List[Vertex]`.
        """
        result: List[Vertex] = List()
        self._vertices.to_first()
        while self._vertices.has_access:
            result.append(self._vertices.content)
            self._vertices.next()
        return result

    @property
    def edges(self) -> List[Edge]:
        """Die Anfrage liefert eine neue Liste aller Kantenobjekte
        vom Typ `List[Edge]`.
        """
        result: List[Edge] = List()
        self._edges.to_first()
        while self._edges.has_access:
            result.append(self._edges.content)
            self._edges.next()
        return result

    def get_vertex(self, id_: str) -> Vertex | None:
        """Die Anfrage liefert das Knotenobjekt mit `id_` als ID.
        Ist ein solchen Knotenobjekt nicht im Graphen enthalten,
        wird `None` zurückgeliefert.
        """
        self._vertices.to_first()
        while self._vertices.has_access:
            if self._vertices.content.id == id_:
                return self._vertices.content
            self._vertices.next()
        return None

    def add_vertex(self, vertex: Vertex | None) -> None:
        """Der Auftrag fügt den Knoten `vertex` in den Graphen ein,
        sofern es noch keinen Knoten mit demselben ID-Eintrag
        wie `vertex` im Graphen gibt und `vertex` eine ID hat, welche nicht `None` ist.
        Ansonsten passiert nichts.
        """
        if vertex is None or vertex.id is None:
            return

        self._vertices.to_first()
        while self._vertices.has_access:
            if self._vertices.content.id == vertex.id:
                return
            self._vertices.next()

        self._vertices.append(vertex)

    def remove_vertex(self, vertex: Vertex) -> None:
        """Der Auftrag entfernt den Knoten `vertex` aus dem Graphen
        und löscht alle Kanten, die mit ihm inzident sind.
        Ist der Knoten `vertex` nicht im Graphen enthalten, passiert nichts.
        """
        self._edges.to_first()
        while self._edges.has_access:
            if vertex in self._edges.content.vertices:
                self._edges.remove()
            else:
                self._edges.next()

        self._vertices.to_first()
        while self._vertices.has_access and self._vertices.content is not vertex:
            self._vertices.next()

        if self._vertices.has_access:
            self._vertices.remove()

    def get_edge(self, vertex: Vertex, another_vertex: Vertex) -> Edge | None:
        """Die Anfrage liefert die Kante, welche die Knoten `vertex`
        und `another_vertex` verbindet, als Objekt vom Typ `Edge`.
        Ist der Knoten `vertex` oder der Knoten `another_vertex` nicht
        im Graphen enthalten oder gibt es keine Kante, die beide Knoten verbindet,
        so wird `None` zurückgeliefert.
        """
        self._edges.to_first()
        while self._edges.has_access:
            vertex1, vertex2 = self._edges.content.vertices
            if (vertex1 is vertex and vertex2 is another_vertex) or (
                vertex1 is another_vertex and vertex2 is vertex
            ):
                return self._edges.content
            self._edges.next()
        return None

    def add_edge(self, edge: Edge | None) -> None:
        """Der Auftrag fügt die Kante `edge` in den Graphen ein,
        sofern beide durch die Kante verbundenen Knoten im Graphen enthalten sind,
        nicht identisch sind und noch keine Kante zwischen den Knoten existiert.
        Ansonsten passiert nichts.
        """
        if edge is None:
            return

        vertex1, vertex2 = edge.vertices
        # pylint: disable=R0916
        if (
            vertex1 is not None
            and vertex2 is not None
            and self.get_vertex(vertex1.id) is vertex1
            and self.get_vertex(vertex2.id) is vertex2
            and self.get_edge(vertex1, vertex2) is None
            and vertex1 is not vertex2
        ):
            self._edges.append(edge)

    def remove_edge(self, edge: Edge) -> None:
        """Der Auftrag entfernt die Kante `edge` aus dem Graphen.
        Ist die Kante `edge` nicht im Graphen enthalten, passiert nichts.
        """
        self._edges.to_first()
        while self._edges.has_access:
            if self._edges.content is edge:
                self._edges.remove()
                return
            self._edges.next()

    def set_all_vertex_marks(self, mark: bool) -> None:
        """Der Auftrag setzt die Markierungen aller Knoten des Graphen auf `mark`."""
        self._vertices.to_first()
        while self._vertices.has_access:
            self._vertices.content.mark = mark
            self._vertices.next()

    def all_vertices_marked(self) -> bool:
        """Die Anfrage liefert `True`,
        wenn alle Knoten des Graphen mit `True` markiert sind, ansonsten `False`.
        """
        self._vertices.to_first()
        while self._vertices.has_access:
            if not self._vertices.content.is_marked:
                return False
            self._vertices.next()
        return True

    def set_all_edge_marks(self, mark: bool) -> None:
        """Der Auftrag setzt die Markierungen aller Kanten des Graphen auf `mark`."""
        self._edges.to_first()
        while self._edges.has_access:
            self._edges.content.mark = mark
            self._edges.next()

    def all_edges_marked(self) -> bool:
        """Die Anfrage liefert `True`,
        wenn alle Kanten des Graphen mit `True` markiert sind, ansonsten `False`.
        """
        self._edges.to_first()
        while self._edges.has_access:
            if not self._edges.content.mark:
                return False
            self._edges.next()
        return True

    def get_neighbours(self, vertex: Vertex) -> List[Vertex]:
        """Die Anfrage liefert alle Nachbarn des Knotens `vertex`
        als neue Liste vom Typ `List[Vertex]`.
        Hat der Knoten `vertex` keine Nachbarn in diesem Graphen
        oder ist gar nicht in diesem Graphen enthalten,
        so wird eine leere Liste zurückgeliefert.
        """
        result: List[Vertex] = List()

        self._edges.to_first()
        while self._edges.has_access:
            vertex1, vertex2 = self._edges.content.vertices
            if vertex is vertex1:
                result.append(vertex2)
            elif vertex is vertex2:
                result.append(vertex1)
            self._edges.next()
        return result

    def get_edges(self, vertex: Vertex) -> List[Edge]:
        """Die Anfrage liefert eine neue Liste alle inzidenten Kanten
        zum Knoten `vertex`.
        Hat der Knoten `vertex` keine inzidenten Kanten in diesem Graphen
        oder ist gar nicht in diesem Graphen enthalten,
        so wird eine leere Liste zurückgeliefert.
        """
        result: List[Edge] = List()

        self._edges.to_first()
        while self._edges.has_access:
            if vertex in self._edges.content.vertices:
                result.append(self._edges.content)
            self._edges.next()
        return result

    @property
    def is_empty(self) -> bool:
        """Die Anfrage liefert `True`, wenn der Graph keine Knoten enthält,
        ansonsten `False`.
        """
        return self._vertices.is_empty
