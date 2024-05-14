""":demand: F1.8"""

from typing import TypeVar

T = TypeVar('T')


class Array:
    def __init__(self, size: int) -> None:
        self.__array = [None for _ in range(size)]
        self.__size = size

    @property
    def length(self) -> int:
        """
        Returns the length of the Array.

        :return: int
        """
        return self.__size

    def get(self, index: int) -> T:
        """
        Returns the value at the `index` position.

        :param index: int
        :return: Object
        """
        return self.__array[index]

    def set(self, index: int, e: T) -> None:
        """
        Sets the value at the `index` position.

        :param index: int
        :param e: Object
        :return: None
        """
        self.__array[index] = e

    def index(self, v: T) -> int:
        """
        Returns the index of the element `e` in the array. Raises ValueError if `e` is not in the array.

        :param v: Object
        :return: int
        """
        try:
            return self.__array.index(v)
        except ValueError:
            raise ValueError(f"{v} is not in array")

    def __str__(self):
        if self.length == 0:
            return "[]"
        string: str = "[{}".format(self.get(0))
        for i in range(1, self.length):
            string += ", {}".format(self.get(i))
        return string + "]"

    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def __eq__(self, other: T) -> bool:
        if not isinstance(other, Array) or self.length != other.length:
            return False
        for i in range(self.length):
            if self[i] != other[i]:
                return False
        return True

    def __len__(self) -> int:
        return self.length

    def __to_visu__(self):
        if self.length == 0:
            return ""
        string: str = "{}".format(self.get(0))
        for i in range(1, self.length):
            string += ",{}".format(self.get(i))
        return string


def Array_length(array: Array) -> int:
    return array.length


def Array_get(array: Array, index: int) -> T:
    return array.get(index)


def Array_set(array: Array, index: int, e: T) -> None:
    array.set(index, e)
