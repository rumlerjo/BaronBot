from player import Player
from railroad import Road
import networkx

class Space:
    """
    A class to represent a space that a piece can be on
    """
    # maybe i should consistently do this lol
    __slots__ = ["road", "position", "region", "occupiedBy"]
    
    def __init__(self, road: Road, name: str, region: str) -> None:
        self.road = road
        self.position = name
        self.region = region # should this be abv or full?
        self.occupiedBy: Player = None
        # getters and setters or just directly . index it?


class Board:
    """
    A class to represent the board the game is played on
    """
    __slots__ = ["graph"]

    def __init__(self) -> None:
        self.graph = networkx.graph.Graph()