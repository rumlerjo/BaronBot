"""
Trip class implementation for tracking a player's trip on the board
@author John Rumler https://github.com/rumlerjo
"""

from typing import Any, List

from Models.board import Space, CitySpace

class Trip:
    """A class representing a trip a player has made from start to destination"""
    def __init__(self, start: CitySpace, end: CitySpace) -> None:
        """
        :param start: The starting Space denoted with a city
        :param end: The ending Space denoted with a city
        """
        self._path = List[Space]
        self._start = start
        self._end = end
    
    def add_space(self, space: Space) -> None:
        self._path.append(space)

    def calculate_cost(self) -> int:
        pass
    
    def __getitem__(self, idx: int) -> Space:
        return self._path[idx]
