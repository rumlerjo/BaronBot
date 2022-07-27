"""
Game player class implementation
@author John Rumler https://github.com/rumlerjo
"""

from interactions import Snowflake, User
from typing import TypeVar, Union

T = TypeVar("T")
Player = TypeVar("Player")

class Player:
    """
    The board game player representing current affairs of each player
    """

    __slots__ = ["_user", "name", "_cash", "_superchief", "_express", 
    "_space", "_current_trip"]

    def __init__(self, user: User, player_data: dict = None) -> None:
        if not player_data:
            self._user = user
            self.name = user.nick
            self._cash = 20000
            self._superchief = False
            self._express = False
            self._space = None
            self._current_trip = None
        
    def __eq__(self, player: Union[str, Snowflake, User]) -> bool:
        if type(player) == str:
            return player == self._user.username or player == str(self._user.id)
        if type(player) == Snowflake:
            return player == self._user.id
        if type(player) == User:
            return player.id == self._user.id # best unique identifier
        return False
    
    def get_cash(self):
        return self._cash

    def add_cash(self, amount: int) -> None:
        """
        Add to cash of player
        :param amount: amount to add
        :return: None
        """
        self._cash += amount

    def sub_cash(self, amount: int) -> None:
        """
        Subtract cash from player
        :param amount: amount to subtract
        :return: None
        """
        self._cash -= amount
    
    def has_chief(self) -> bool:
        """
        Check if player has a superchief
        :return: Bool representing whether player has superchief
        """
        return self._superchief

    def buy_express(self) -> None:
        """
        Give player an express and subtract the cost
        :return: None
        """
        if self.get_cash() >= 4000:
            self.sub_cash(4000)
            self._express = True
    
    def buy_chief(self) -> None:
        """
        Give player a superchief and subtract the cost
        :return: None
        """
        if self.get_cash() >= 40000:
            self.sub_cash(40000)
            self._superchief = True

    
"""
TO ADD
once linkedlist is complete to spec DO
make linkedlist of current trip taken
make getter for current trip (if necessary?)
calculate how many roads have been ridden
do getters and setters for space
"""