"""
Bot game class implementation
@author John Rumler https://github.com/rumlerjo
"""

from typing import TypeVar, List, Union, Optional
from Models.railroad import Road
from interactions import Snowflake, User
from Models.settings import Settings
from Models.player import Player

class Game:
    def __init__(self, guild: Snowflake, settings: Settings, gameWindow: Union[int, str]) -> None:
        self._players: List[Player] = list()
        self._guildId = guild
        self._gameWindow = str(gameWindow) # the main message window
        self._current_player = 0 # idx of current player
        self._settings = settings
    
    def add_player(self, player: Player) -> None:
        """
        Add a player to the game
        :param player: The player object to add to game
        """
        self._players.append(player)

    def get_player(self, player: Union[str, Snowflake, User]) -> Optional[Player]:
        """
        Find a player by id in game, or return None
        :param playerId: 
        """
        if player in self._players:
            return self._players[self._players.index(player)]
    
    
    def print_roads(self) -> None:
        """
        Print out all roads
        :return: None
        """
        for i, road in enumerate(self._roads):
            print(f"[{i}] " + str(road))

    def str_roads(self) -> str:
        """
        Get a string with road info
        :return: String with all road info
        """
        out = ""
        for i, road in enumerate(self._roads):
            out += f"[{i}] " + str(road)
        return out



