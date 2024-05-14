""":demand: F1.8"""

from typing import Optional, TypeVar
import sys
from .TreeNode import TreeNode

T = TypeVar('T')


class BinaryTreeNode(TreeNode):
    """
    A node that can be linked to two other nodes.
    """

    def __init__(self, value: Optional[T] = None, left_child: Optional[TreeNode] = None,
                 right_child: Optional[TreeNode] = None):
        super().__init__(value, [left_child, right_child])

    @property
    def left_child(self) -> Optional[TreeNode]:
        """
        Returns the left child of this node. Can be None.

        :return: BinaryTreeNode
        """
        return self.children[0]

    @left_child.setter
    def left_child(self, node: Optional[TreeNode]) -> None:
        """
        Sets the left child of this node.

        :param node: The new left child.
        :return: None
        """
        self.children.set(0, node)

    @property
    def right_child(self) -> Optional[TreeNode]:
        """
        Returns the right child of this node. Can be None.

        :return: BinaryTreeNode
        """
        return self.children[1]

    @right_child.setter
    def right_child(self, node: Optional[TreeNode]) -> None:
        """
        Sets the right child of this node.

        :param node: The new right child.
        :return: None
        """
        self.children.set(1, node)

    @property
    def value(self) -> T:
        """
        Returns the value of this node. Can be None.

        :return: Object
        """
        return self._value

    @value.setter
    def value(self, e: T) -> None:
        """
        Sets the value of this node.

        :param e: Object
        :return: T
        """
        self._value = e

    def has_child(self) -> bool:
        """
        Tells if this node has at least one child node.

        :return: bool
        """
        return self.left_child is not None or self.right_child is not None

    def __str__(self) -> str:
        return "↙{}↘".format(self.value)

    def __to_visu__(self) -> str:
        return None if self.is_sentinel() else {"data" : self.value, "children" : [child.__to_visu__() for child in filter(lambda c : c is not None and not c.is_sentinel(), self.children)]}


def BinaryTreeNode_value(node: BinaryTreeNode) -> T:
    return node.value


def BinaryTreeNode_set_value(node: BinaryTreeNode, value: T) -> None:
    node.value = value


def BinaryTreeNode_next(node: BinaryTreeNode) -> Optional[TreeNode]:
    return print("Don't use this function ! Use BinaryTreeNode_right_child instead.", file=sys.stderr)


def BinaryTreeNode_set_next(node: BinaryTreeNode, next: TreeNode) -> Optional[TreeNode]:
    return print("Don't use this function ! Use BinaryTreeNode_set_right_child instead.", file=sys.stderr)


def BinaryTreeNode_has_next(node: BinaryTreeNode) -> bool:
    return print("Don't use this function ! Use BinaryTreeNode_has_child instead.", file=sys.stderr) is not None


def BinaryTreeNode_sentinel() -> Optional['BinaryTreeNode']:
    return BinaryTreeNode.sentinel()


def BinaryTreeNode_is_sentinel(node: BinaryTreeNode) -> bool:
    return node.is_sentinel()


def BinaryTreeNode_left_child(node: BinaryTreeNode) -> Optional[TreeNode]:
    return node.left_child


def BinaryTreeNode_set_left_child(node: BinaryTreeNode, left_child: TreeNode) -> None:
    node.left_child = left_child


def BinaryTreeNode_right_child(node: BinaryTreeNode) -> Optional[TreeNode]:
    return node.right_child


def BinaryTreeNode_set_right_child(node: BinaryTreeNode, right_child: TreeNode) -> None:
    node.right_child = right_child


def BinaryTreeNode_has_child(node: BinaryTreeNode) -> bool:
    return node.has_child()
