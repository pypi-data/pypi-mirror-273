""":demand: F1.8"""

from collections.abc import Iterable
from typing import TypeVar
import inspect
from .DoublyLinkedList import DoublyLinkedList

T = TypeVar('T')


class RestrictedDoublyLinkedList:
    def __init__(self, doubly_linked_list):
        self.__doubly_linked_list: DoublyLinkedList = doubly_linked_list

    @property
    def length(self):
        return self.__doubly_linked_list.length

    def is_empty(self) -> bool:
        return self.__doubly_linked_list.length == 0

    def get(self, index: int) -> T:
        return self.__doubly_linked_list.get(index)

    def index(self, v: T) -> int:
        return self.__doubly_linked_list.index(v)

    def __str__(self) -> str:
        return str(self.__doubly_linked_list)

    def __getitem__(self, index: int) -> T:
        return self.__doubly_linked_list[index]

    def __eq__(self, other):
        return self.__doubly_linked_list == other or (hasattr(other,
                                                              "_RestrictedDoublyLinkedList__doubly_linked_list") and self.__doubly_linked_list == other.__doubly_linked_list)

    def __len__(self) -> int:
        return self.__doubly_linked_list.length

    def __iter__(self):
        return self.__doubly_linked_list.__iter__()

    def __to_visu__(self) -> str:
        return self.__doubly_linked_list.__to_visu__()

    def insert_last(self, value):
        if not isinstance(inspect.currentframe().f_back.f_locals.get('self'), Graph):
            raise AttributeError("Method 'insert_last' can only be called from 'Graph'.")
        return self.__doubly_linked_list.insert_last(value)

    def delete(self, index):
        if not isinstance(inspect.currentframe().f_back.f_locals.get('self'), Graph):
            raise AttributeError("Method 'delete' can only be called from 'Graph'.")
        return self.__doubly_linked_list.delete(index)


class Graph:
    def __init__(self, it: Iterable[T] = None):
        self.__vertices: RestrictedDoublyLinkedList = RestrictedDoublyLinkedList(DoublyLinkedList(it))
        self.__nb_vertices: int = self.__vertices.length
        self.__nb_max_vertices: int = max(5, self.__nb_vertices)
        self.__edges: list[list[int]] = [[0 for _ in range(self.__nb_max_vertices)] for _ in
                                         range(self.__nb_max_vertices)]

    @property
    def vertices(self) -> RestrictedDoublyLinkedList:
        return self.__vertices

    @property
    def edges(self) -> list[list[int]]:
        return self.__edges

    def add_vertex(self, v: T) -> None:
        """
        Add a vertex to the graph.

        :param v: The vertex to add.
        """
        if self.__nb_vertices >= self.__nb_max_vertices:
            self.__nb_max_vertices *= 2
            for _ in range(self.__nb_max_vertices - self.__nb_vertices):
                self.__edges.append([0 for _ in range(self.__nb_max_vertices)])
            for i in range(self.__nb_vertices):
                self.__edges[i] += [0] * (self.__nb_max_vertices - self.__nb_vertices)
        self.__vertices.insert_last(v)
        self.__nb_vertices += 1

    def remove_vertex(self, index: int) -> None:
        """
        Remove a vertex from the graph.

        :param index: The index of the vertex to remove.
        """
        self.__vertices.delete(index)
        self.__edges.pop(index)
        for i in range(self.__nb_max_vertices - 1):
            self.__edges[i].pop(index)
        self.__nb_vertices -= 1
        self.__nb_max_vertices -= 1

    def get_vertex(self, index: int) -> T:
        """
        Get the value of a vertex from the graph.

        :param index: The index of the vertex to get.
        """
        return self.__vertices[index]

    def add_edge(self, index1: int, index2: int) -> None:
        """
        Add an oriented edge to the graph.

        :param index1: The index of the first vertex's index to add and edge to.
        :param index2: The index of the second vertex's index to add and edge to.
        """
        if index1 >= self.__nb_vertices or index2 >= self.__nb_vertices:
            raise IndexError
        self.__edges[index1][index2] += 1

    def remove_edge(self, index1: int, index2: int) -> None:
        """
        Remove an oriented edge from the graph.

        :param index1: The index of the first vertex's index to remove and edge to.
        :param index2: The index of the second vertex's index to remove and edge to.
        """
        if index1 >= self.__nb_vertices or index2 >= self.__nb_vertices:
            raise IndexError
        self.__edges[index1][index2] -= 1

    def has_edge(self, index1: int, index2: int) -> bool:
        """
        Check if an oriented edge exists between two vertices.

        :param index1: The index of the first vertex's index to check.
        :param index2: The index of the second vertex's index to check.
        """
        if index1 >= self.__nb_vertices or index2 >= self.__nb_vertices:
            raise IndexError
        return self.edges[index1][index2] > 0

    def __str__(self) -> str:
        return "{}\n{}".format(str(self.__vertices), "\n".join([str(l) for l in self.__edges]))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Graph) or self.__vertices != other.__vertices:
            return False
        for i in range(self.__nb_vertices):
            for j in range(self.__nb_vertices):
                if self.__edges[i][j] != other.__edges[i][j]:
                    return False
        return True

    def __to_visu__(self) -> str:
        if self.__nb_vertices == 0 :
            return "&"
        
        edges = ""
        for i in self.__edges:
            for j in i:
                edges += str(j)
                edges += ","
            edges = edges[:-1]
            edges += ";"
        edges = edges[:-1]

        return  self.__vertices.__to_visu__() + "&" + edges


def Graph_add_vertex(graph: Graph, v: T) -> None:
    return graph.add_vertex(v)


def Graph_remove_vertex(graph: Graph, index: int) -> None:
    return graph.remove_vertex(index)


def Graph_get_vertex(graph: Graph, index: int) -> T:
    return graph.get_vertex(index)


def Graph_add_edge(graph: Graph, index1: int, index2: int) -> None:
    return graph.add_edge(index1, index2)


def Graph_remove_edge(graph: Graph, index1: int, index2: int) -> None:
    return graph.remove_edge(index1, index2)


def Graph_has_edge(graph: Graph, index1: int, index2: int) -> bool:
    return graph.has_edge(index1, index2)
