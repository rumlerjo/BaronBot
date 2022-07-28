"""
Adjacency Graph class implementation
@author John Rumler https://github.com/rumlerjo
"""


# networkx and easygraph were not customized enough for my liking.
# this will be a simple doubly-associated adjacency graph (see what my neighbor is!)
from typing import Any, Dict, Hashable, List, TypeVar, Optional
from copy import deepcopy

GraphNode = TypeVar("GraphNode")
AdjacencyGraph = TypeVar("AdjacencyGraph")
NoStringConversion = TypeVar("NoStringConversion")
InvalidGraphOperation = TypeVar("InvalidGraphOperation")

class NoStringConversion(Exception):
    pass

class InvalidGraphOperation(Exception):
    pass

class GraphNode:
    """
    An adjacency graph node
    """

    __slots__ = ["_id", "_data", "_adj", "_degree"]

    def __init__(self, id: str, data: Any) -> None:
        # requires data to have a string method for printing purposes
        """
        :param id: String identifier for this node
        :param data: The data that the node container holds. Must have a str method.
        :return: None
        """
        try:
            str(data)
        except:
            raise NoStringConversion("Passed node data could not be converted to string.")
        self._id = str(id) if type(id) != str else id
        self._data = data
        self._adj: Dict[str, GraphNode] = dict()
        self._degree = 0

    def adjacent(self) -> Dict[str, GraphNode]:
        """
        Return the adjacency dict
        :return: Adjacent node dict
        """
        return self._adj
    
    def add_adjacent(self, id: str, node: GraphNode) -> None:
        """
        Add a node to the adjacency dict
        :param id: The id of the node to add
        :param node: The node to associate with the id
        :return: None
        """
        if not self._adj.get(id):
            self._adj[id] = node
            self._degree += 1
    
    def connect(self, otherNode: GraphNode) -> None:
        """
        Create forward and backward adjacency between this node and another node
        :param otherNode: The node to connect this node to
        :return: None
        """
        # if it's adjacent one way, it should be the other as well.
        self.add_adjacent(otherNode.id(), otherNode)
        otherNode.add_adjacent(self.id(), otherNode)
    
    def disconnect(self, otherNode: GraphNode) -> None:
        """
        Remove forward and backward adjacency between this node and another node
        :param otherNode: The node to disconnect this node from
        :return: None
        """
        if self.adjacent().get(otherNode.id()):
            self.adjacent().pop(otherNode.id())
        if otherNode.adjacent().get(self.id()):
            otherNode.adjacent().pop(self.id())
    
    def id(self) -> str:
        """
        :return: Id of node
        """
        return self._id
    
    def degree(self) -> int:
        """
        :return: number of adjacent nodes
        """
        return self._degree

    def str_adj(self) -> str:
        return self.id() + str(self._adj)

    def __str__(self) -> str:
        return "Node " + self.id() + " with data " + str(self._data)

    def __repr__(self) -> str:
        return str(self)

class AdjacencyGraph:
    """
    A non-directed Node-based adjacency matrix with 2-sided association.\n
    In order to be simple it is missing a lot of features like bfs, dfs, and circular checking.
    """

    __slots__ = ["_size", "_nodes"]

    def __init__(self) -> None:
        self._nodes: Dict[str, GraphNode] = dict()

    # personally prefer that it returns the node, so if I add it I can play around with it.
    def add_node(self, node: Optional[GraphNode] = None, nodeId: Optional[str] = None, 
    nodeData: Optional[Any] = None) -> GraphNode:
        """
        Add a node to the graph
        :param node: (Optional) A GraphNode to insert
        :param nodeId: (Optional if node present) The Id of the node to insert
        :param nodeData: (Optional if node present) The data of the node to insert
        :return: The node added to the graph
        """
        # this will also update node at whatever id is specified, trying to avoid duplicate Ids
        if node and type(node) == GraphNode:
            self[node.id()] = node
            return node
        elif nodeId and nodeData and (type(nodeId) == str or str(nodeId)):
            new_node = GraphNode(nodeId, nodeData)
            self._nodes[nodeId] = new_node
            return new_node
        else:
            raise InvalidGraphOperation("Invalid parameters supplied to member function 'add_node()'")
        
    def add_nodeless_adjacency(self, id1: str, id2: str, data1: Any, data2: Any) -> None:
        """
        Add adjacency supplying only ids and data rather than nodes (creates 2 nodes)
        :param id1: Id of first node
        :param id2: Id of second node
        :param data1: Data of first node
        :param data2: Data of second node
        """
        node1 = self.add_node(nodeId = id1, nodeData = data1)
        node2 = self.add_node(nodeId = id2, nodeData = data2)
        node1.connect(node2)

    def add_node_adjacency(self, node1: GraphNode, node2: GraphNode) -> None:
        """
        Add adjacency supplying 2 nodes
        :param node1: The first node to connect
        :param node2: The second node to connect
        """
        if not node1 in self._nodes:
            self.add_node(node = node1)
        if not node2 in self._nodes:
            self.add_node(node = node2)
        node1.connect(node2)

    def __getitem__(self, id: Hashable) -> GraphNode:
        """
        The same as self._nodes[id], but allows direct indexing of class object
        :param id: Id of node to find
        :return: Found node or none
        """
        try:
            str(id)
        except:
            raise InvalidGraphOperation("Key supplied for indexing is not hashable")
        item = self._nodes.get(str(id))
        if not item:
            raise InvalidGraphOperation("Key supplied for index has no associated value")
        return item
    
    def __setitem__(self, key: Hashable, val: Any) -> None:
        """
        Item assignment, allows self._nodes[id] = data directly from class object
        :param key: Key to assign with
        :param val: Value to assign to key
        :return: None
        """
        try:
            str(key)
        except:
            raise InvalidGraphOperation("Key given to item assignment not hashable")
        self._nodes[key] = val
    
    def __str__(self) -> str:
        # will improve this probably
        return str(self._nodes)
    
    def __repr__(self) -> str:
        return str(self)

    def pop_node(self, lookForId: str) -> Optional[GraphNode]:
        """
        O(n) pop of node out of nodes
        :param lookForId: Id of node to remove
        :return: Removed node
        """
        node = self._nodes.get(lookForId)
        if node:
            n: GraphNode = None
            for n in self._nodes.values():
                n.disconnect(node)
            self._nodes.pop(lookForId)
            return node

    def copy(self) -> AdjacencyGraph:
        """
        :return: a deep copy of the graph.
        """
        return deepcopy(self)