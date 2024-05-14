""":demand: F1.8"""

from collections.abc import Iterable
from typing import TypeVar
from .TwoWayNode import TwoWayNode
from .List import List

T = TypeVar('T')


class DoublyLinkedList(List):
    """
    A doubly linked list that consists of a set of sequentially linked TwoWayNode.
    """

    # head <=> ... <=> ... <=> ... <=> sentinel()
    def __init__(self, it: Iterable[T] = None) -> None:
        """
        Initializes the doubly linked list.
        """
        self.__head: TwoWayNode = TwoWayNode.sentinel()
        self.__tail: TwoWayNode = self.__head
        self.__length = 0
        if it is not None:
            for item in it:
                self.insert_last(item)

    @property
    def length(self) -> int:
        """
        Returns the length of the doubly linked list.

        :return: int
        """
        return self.__length

    def is_empty(self) -> bool:
        """
        Checks if the list is empty.

        :return: bool
        """
        return self.length == 0

    def get(self, index: int) -> T:
        """
        Returns the element at the `index` position.

        :param index: int
        :return: Object
        """
        return self._get_node(index).value

    def _get_node(self, index: int) -> TwoWayNode:
        """
        Returns the node at the `index` position.

        :param index: int
        :return: TwoWayNode
        """
        if index < 0 or index >= self.length:
            raise IndexError('Index out of range')
        if index > self.length / 2:
            i: int = self.length - 1
            current_node = self.__tail
            while i > index:
                current_node = current_node.previous
                i -= 1
            return current_node
        i: int = 0
        current_node = self.__head
        while i < index:
            current_node = current_node.next
            i += 1
        return current_node

    def set(self, index: int, e: T) -> None:
        """
        Sets the element at the `index` position as `e`.

        :param index: int
        :param e: Object
        :return: None
        """
        node: T = self._get_node(index)
        node.value = e

    def insert_head(self, e: T) -> None:
        """
        Inserts the element at the head of the list.

        :param e: Object
        :return: None
        """
        new_node = TwoWayNode(e, next_node=self.__head)
        if self.is_empty():
            self.__tail = new_node
        self.__head.previous = new_node
        self.__head = new_node
        self.__length += 1

    def insert_after(self, index: int, e: T) -> None:
        """
        Inserts the element after the given `index`.

        :param index: int
        :param e: Object
        :return: None
        """
        if index == self.__length - 1:
            return self.insert_last(e)
        if index < 0 or index >= self.__length:
            raise IndexError('Index out of range')
        else:
            new_node = TwoWayNode(e)
            index_node = self._get_node(index)
            new_node.next = index_node.next
            new_node.previous = index_node
            index_node.next = new_node
            new_node.next.previous = new_node
        self.__length += 1

    def insert_last(self, e: T) -> None:
        """
        Inserts the element at the last node of the list.

        :param e: Object
        :return: None
        """
        if self.is_empty():
            return self.insert_head(e)
        new_node = TwoWayNode(e)
        # last_node = self._get_node(self.__length - 1)
        tmp_sentinel = self.__tail.next
        self.__tail.next = new_node
        new_node.previous = self.__tail
        new_node.next = tmp_sentinel
        self.__tail = new_node
        self.__length += 1

    def insert(self, index: int, e: T) -> None:
        """
        Inserts the element before the given `index`.

        :param index: int
        :param e: Object
        :return: None
        """
        if index == 0:
            return self.insert_head(e)
        if index < 0 or index >= self.__length:
            raise IndexError('Index out of range')
        else:
            new_node = TwoWayNode(e)
            index_node = self._get_node(index)
            index_node.previous.next = new_node
            new_node.next = index_node
            new_node.previous = index_node.previous
            index_node.previous = new_node

        self.__length += 1

    def delete(self, index: int) -> None:
        """
        Deletes the element at the given `index`.

        :param index: int
        :return: None
        """
        if index < 0 or index >= self.__length:
            raise IndexError('Index out of index')
        if index == 0:
            self.__head = self.__head.next
            self.__head.previous = None
        else:
            current_node = self._get_node(index)
            previous_node = current_node.previous
            previous_node.next = current_node.next
            current_node.next.previous = previous_node
        self.__length -= 1

    def index(self, v: T) -> int:
        """
        Returns the index of the element `e` in the list. Raises ValueError if `e` is not in the list.

        :param v: Object
        :return: int
        """
        i: int = 0
        current_node = self.__head
        while not current_node.is_sentinel() and current_node.value != v:
            current_node = current_node.next
            i += 1
        if current_node.is_sentinel():
            raise ValueError(f'No such element in the list :{v}')
        return i

    def __str__(self) -> str:
        if self.is_empty():
            return "[]"
        else:
            current_node = self.__head
            result = "["
            while not current_node.next.is_sentinel():
                result += current_node.__to_visu__() + " ↔ "
                current_node = current_node.next
            result += current_node.__to_visu__() + "]"
            return result

    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __eq__(self, other):
        if not isinstance(other, DoublyLinkedList) or self.__length != other.__length:
            return False
        current = self.__head
        other_current = other.__head
        while not current.is_sentinel():
            if current.value != other_current.value:
                return False
            current = current.next
            other_current = other_current.next
        return True

    def __len__(self) -> int:
        return self.__length

    def __iter__(self):
        current = self.__head
        while not current.is_sentinel():
            yield current.value
            current = current.next

    def __to_visu__(self) -> str:
        if self.is_empty():
            return ""
        current_node = self.__head
        result = ""
        while not current_node.next.is_sentinel():
            result += str(current_node.value) + ','
            current_node = current_node.next
        return result + str(current_node.value)


def DoublyLinkedList_length(list: DoublyLinkedList) -> int:
    return list.length


def DoublyLinkedList_get(list: DoublyLinkedList, index: int) -> T:
    return list.get(index)


def DoublyLinkedList_insert(list: DoublyLinkedList, index: int, e: T) -> None:
    list.insert(index, e)


def DoublyLinkedList_delete(list: DoublyLinkedList, index: int) -> None:
    list.delete(index)


def DoublyLinkedList_is_empty(list: DoublyLinkedList) -> bool:
    return list.is_empty()


def DoublyLinkedList_set(list: DoublyLinkedList, index: int, e: T) -> None:
    list.set(index, e)


def DoublyLinkedList_insert_head(list: DoublyLinkedList, e: T) -> None:
    list.insert_head(e)


def DoublyLinkedList_insert_last(list: DoublyLinkedList, e: T) -> None:
    list.insert_last(e)


def DoublyLinkedList_insert_after(list: DoublyLinkedList, index: int, e: T) -> None:
    list.insert_after(index, e)


def DoublyLinkedList__get_node(list: DoublyLinkedList, index: int) -> TwoWayNode:
    return list._get_node(index)
