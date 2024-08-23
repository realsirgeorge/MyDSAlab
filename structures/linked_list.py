"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""
from __future__ import annotations
from typing import Any, Optional
class Node:
    """
    A simple type to hold data and a next pointer
    """
    def __init__(self, data: Any) -> None:
        self._data = data  # This is the payload data of the node
        self._next = None  # This is the "next" pointer to the next Node
        self._prev = None  # This is the "previous" pointer to the previous Node

    def set_data(self, data: Any) -> None:
        self._data = data

    def get_data(self) -> Any:
        return self._data

    def set_next(self, node: Node) -> None:
        self._next = node

    def get_next(self) -> Node | None:
        return self._next

    def set_prev(self, node: Node) -> None:
        self._prev = node

    def get_prev(self) -> Node | None:
        return self._prev

class DoublyLinkedList:
    """
    Your doubly linked list code goes here.
    Note that any time you see `Any` in the type annotations,
    this refers to the "data" stored inside a Node.

    [V3: Note that this API was changed in the V3 spec] 
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size: int = 0
        self.is_reversed: bool = False  # Initialize the is_reversed attribute

    def __str__(self) -> str:
        """
        A helper that allows you to print a DoublyLinkedList type
        via the str() method.
        """
        if self.is_reversed:
            current = self.tail
            nodes = []
            while current is not None:
                nodes.append(str(current.get_data()))
                current = current.get_prev()
        else:
            current = self.head
            nodes = []
            while current is not None:
                nodes.append(str(current.get_data()))
                current = current.get_next()
        
        return " <-> ".join(nodes)

    """
    Simple Getters and Setters below
    """
    def get_size(self) -> int:
        """
        Return the size of the list.
        Time complexity for full marks: O(1)
        """
        return self.size

    def get_head(self) -> Any | None:
        """
        Return the data of the leftmost node in the list, if it exists.
        Time complexity for full marks: O(1)
        """
        if self.head is None:
            return None
        return self.head.get_data()

    def set_head(self, data: Any) -> None:
        """
        Replace the leftmost node's data with the given data.
        If the list is empty, do nothing.
        Time complexity for full marks: O(1)
        """
        if self.head is not None:
            self.head.set_data(data)       

    def get_tail(self) -> Any | None:
        """
        Return the data of the rightmost node in the list, if it exists.
        Time complexity for full marks: O(1)
        """
        if self.tail is None:
            return None
        return self.tail.get_data()

    def set_tail(self, data: Any) -> None:
        """
        Replace the rightmost node's data with the given data.
        If the list is empty, do nothing.
        Time complexity for full marks: O(1)
        """
        if self.tail is not None:
            self.tail.set_data(data)

    """
    More interesting functionality now.
    """

    def insert_to_front(self, data: Any) -> None:
        """
        Insert the given data to the front of the list.
        Hint: You will need to create a Node type containing
        the given data.
        Time complexity for full marks: O(1)
        """
        # if self.is_reversed:
        #     self.insert_to_back(data)
        # else:
            # Original implementation for inserting at the front
        new_node = Node(data)
        if self.head is None:
                self.head = new_node
                self.tail = new_node
        else:
                new_node.set_next(self.head)
                self.head.set_prev(new_node)
                self.head = new_node
        self.size += 1

    def insert_to_back(self, data: Any) -> None:
        """
        Insert the given data (in a node) to the back of the list
        Time complexity for full marks: O(1)
        """
        # if self.is_reversed:
        #     self.insert_to_front(data)
        # else:
            # Original implementation for inserting at the back
        new_node = Node(data)
        if self.tail is None:
                self.head = new_node
                self.tail = new_node
        else:
                new_node.set_prev(self.tail)
                self.tail.set_next(new_node)
                self.tail = new_node
        self.size += 1

    def remove_from_front(self) -> Any | None:
        """
        Remove the front node, and return the data it holds.
        Time complexity for full marks: O(1)
        """
        if self.head is None:
            return None
        data = self.head.get_data()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.get_next()
            self.head.set_prev(None)
        self.size -= 1
        return data

    def remove_from_back(self) -> Any | None:
        """
        Remove the back node, and return the data it holds.
        Time complexity for full marks: O(1)
        """
        if self.tail is None:
            return None
        data = self.tail.get_data()
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.get_prev()
            self.tail.set_next(None)
        self.size -= 1
        return data

    def find_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list and returns True
        if a match is found; False otherwise.
        Time complexity for full marks: O(N)
        """
        current = self.head
        while current is not None:
            if current.get_data() == elem:
                return True
            current = current.get_next()
        return False

    def find_and_remove_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list; if a match is
        found, this node is removed from the linked list, and True is returned.
        False is returned if no match is found.
        Time complexity for full marks: O(N)
        """
        current = self.head
        while current is not None:
            if current.get_data() == elem:
                if current.get_prev() is not None:
                    current.get_prev().set_next(current.get_next())
                else:
                    self.head = current.get_next()

                if current.get_next() is not None:
                    current.get_next().set_prev(current.get_prev())
                else:
                    self.tail = current.get_prev()

                self.size -= 1
                return True
            current = current.get_next()
        return False

    def reverse(self) -> None:
        """
        Reverses the linked list
        Time complexity for full marks: O(1)
        """
        self.is_reversed = not self.is_reversed
