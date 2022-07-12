from typing import Any, Optional, TypeVar, Union

from board import Space, CitySpace

Node = TypeVar("Node")
LLIter = TypeVar("LLIter")
LinkedList = TypeVar("LinkedList")

class LinkedListOutOfRange(Exception):
    pass


class Node:
    """
    A linked-node class
    """
    def __init__(self, value: Any, parent: Node = None, child: Node = None) -> None:
        """
        :param value: Value of the node
        :param parent: Previous node
        :param child: Next node
        """
        self.prev = parent
        self.next = child
        self.value = value # this will be a space with road info and such
    
    def __eq__(self, o: Union[Node, Any]) -> bool:
        if type(o) == Node:
            return self == Node # will this work?
        elif type(o) == type(self.value):
            return self.value == o
        return False

    def __str__(self) -> str:
        return "Node with value: " + str(self.value)
    
    def __repr__(self) -> str:
        return str(self)

class LinkedList:
    """
    A linked list class
    """
    def __init__(self, head: Node = None, tail: Node = None) -> None:
        self._head = head
        self._tail = tail
        self._size = 0

    def __str__(self) -> str:
        out = str()
        for i in range(len(self)):
            if i == len(self) - 1:
                out += str(self[i].value)
            else:
                out += str(self[i].value) + " -> "
        return out
    
    def __repr__(self) -> str:
        return str(self)

    def __getitem__(self, idx: int) -> Optional[Node]:
        """
        Indexing by number
        O(n)
        """
        if idx < 0:
            if idx + len(self) >= 0:
                curr = self._tail
                for _ in range(abs(idx)):
                    curr = curr.prev
                return curr
        elif 0 <= idx < len(self):
            curr = self._head
            for _ in range(idx):
                curr = curr.next
            return curr
        raise LinkedListOutOfRange("Attempted to index list out of range.")

    def __len__(self) -> int:
        """
        Return the number of elements in the linked list
        """
        return self._size

    def insert(self, value: Union[Node, Any], position: int = 0) -> bool:
        """
        Insert a Node at the given position.
        The current node at the given position moves one to the right
        To push to the end, use push
        :param value: Value or Node to insert
        :position: Position to insert at, defaults to front of list
        :return: True if insert was successful, false if not
        """
        replace = self[position]
        if replace:
            new_node: Node = None
            if type(value) == Node:
                new_node = value
                new_node.prev = replace.prev
                new_node.next = replace
            else:
                new_node = Node(value, replace.prev, replace)
            if self._head == replace:
                self._head = new_node
            replace.prev = new_node
            if replace.prev.prev:
                replace.prev.prev.next = new_node
            self._size += 1
            return True
        elif not replace and len(self) == 0:
            new_node: Node = None
            if type(value) == Node:
                new_node = value
            else:
                new_node = Node(value)
            self._head = new_node
            self._tail = new_node
            self._size += 1
            return True
        return False

    def push(self, value: Union[Node, Any], append: bool = True) -> bool:
        """
        Push a Node to the back or front of the linked list
        :param value: The value or Node to push
        :param append: Whether to append or prepend the Node
        :return: Whether the push succeeded or not
        """
        if not append:
            return self.insert(value)
        
        new_node: Node = None
        if type(value) == Node:
            new_node = value
        else:
            new_node = Node(value)
        
        if len(self) == 0:
            self._head = new_node
            self._tail = new_node
        elif len(self) == 1:
            self._tail = new_node
            new_node.prev = self._head
            self._head.next = self._tail
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        
        self._size += 1
        return True

    def head(self) -> Node:
        return self._head
    
    def tail(self) -> Node:
        return self._tail
    
    def pop(self, position: Optional[int] = None) -> Optional[Node]:
        """
        Pop a Node out of the list
        :param position: The index of the Node to remove
        :return: Removed Node
        """
        if len(self) == 0:
            return

        if position:
            to_remove = self[position]
            if to_remove.prev:
                to_remove.prev.next = to_remove.next
            if to_remove.next:
                to_remove.next.prev = to_remove.prev
            to_remove.prev = None
            to_remove.next = None
            self._size -= 1
            return to_remove
        
        to_remove = self._tail
        if len(self) == 1:
            self._head = None
            self._tail = None
        self._tail = to_remove.prev
        to_remove.prev = None
        self._size -= 1
        return to_remove

    class LLIter:
        """An iterator class for Linked List"""
        def __init__(self, linkedList: LinkedList) -> None:
            self._list = linkedList
            self._current_node = linkedList.head()
        
        def __next__(self) -> Node:
            if self._current_node.next:
                self._current_node = self._current_node.next
                return self._current_node
            return StopIteration
    
    def __iter__(self) -> LLIter:
        return LLIter(self)

class Trip:
    """A class representing a trip a player has made from start to destination"""
    def __init__(self, start: CitySpace, end: CitySpace) -> None:
        """
        :param start: The starting Space denoted with a city
        :param end: The ending Space denoted with a city
        """
        self._path = LinkedList()
        self._start = start
        self._end = end
    
    def add_space(self, space: Space) -> None:
        self._path.push(space)
    
    def path_to_list(self) -> list[Space]:
        path = list()
        for i in range(len(self._path)):
            path.append(self._path[i])
        return path

    def calculate_cost(self) -> int:
        pass
    
    def __getitem__(self, idx: int) -> Space:
        return self._path[idx]
