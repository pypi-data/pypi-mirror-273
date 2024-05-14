""":demand: F1.8"""

from typing import TypeVar
from abc import ABC, abstractmethod
from collections.abc import Iterable

T = TypeVar('T')


class List(ABC, Iterable[T]):
    @property
    @abstractmethod
    def length(self) -> int:
        """
        Returns the length of the list.

        :return: int
        """

    @abstractmethod
    def get(self, index: int) -> T:
        """
        Returns the element at the `index` position.

        :param index: int
        :return: Object
        """

    @abstractmethod
    def insert(self, index: int, e: T) -> None:
        """
        Inserts the element after the given `index`.

        :param index: int
        :param e: Object
        :return: None
        """

    @abstractmethod
    def delete(self, index: int) -> None:
        """
        Deletes the element at the given `index`.

        :param index: int
        :return: None
        """

    @abstractmethod
    def index(self, v: T) -> int:
        """
        Returns the index of the element `e` in the list. Raises ValueError if `e` is not in the list.

        :param v: Object
        :return: int
        """
