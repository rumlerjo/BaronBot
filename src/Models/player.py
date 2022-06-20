from game import Game
from interactions import GuildMember
from typing import TypeVar

T = TypeVar("T")
Player = TypeVar("Player")

class Player:
    """
    The board game player representing current affairs of each player
    """
    def __init__(self, game: Game, user: GuildMember, player_data: dict = None) -> None:
        if not player_data:
            self._user = user
            self._name = user.nick
            self._game = game
            self._cash = 20000
            self._space = None
            self._current_trip = None
    
    def get_cash(self):
        return self._cash

    def set_cash(self, amount: int) -> None:
        """
        A setter for player cash
        :param amount: amount to change cash to
        :return: None
        """
        self._cash = amount
    
"""
TO ADD
once linkedlist is complete to spec DO
make linkedlist of current trip taken
make getter for current trip (if necessary?)
calculate how many roads have been ridden
do getters and setters for space
"""