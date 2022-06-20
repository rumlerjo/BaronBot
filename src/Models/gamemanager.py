from http import server
from Models.player import Player
from typing import Dict, List
from Models.game import Game

class GameManager:
    """A container to manage games"""
    def __init__(self) -> None:
        self._games = Dict[str, Dict[str, Game]]
    
    def add_game(self, game: Game, serverId: int | str, gameWindow: int | str) -> bool:
        """
        Add a game to the manager
        :param game: The game object to add
        :param serverId: A representation of the server the game is played in
        :param gameWindow: A representation of the message the game is played on
        :return: Bool indicating whether game was added or not
        """
        serverId = str(serverId)
        gameWindow = str(gameWindow)
        if self._games.get(serverId):
            if self._games[serverId].get(gameWindow):
                return False
        self._games[serverId][gameWindow] = game
        return True
