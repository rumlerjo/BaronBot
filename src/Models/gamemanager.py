from http import server
from Models.player import Player
from typing import Dict, List, Union
from Models.game import Game

class GameManager:
    """A container to manage games"""
    def __init__(self) -> None:
        self._games = Dict[str, Dict[str, Game]]
        self._lobbies = Dict[str, Dict[str, Game]]

    def open_lobby(self, serverId: Union[int, str], lobbyMsg: Union[int, str]) -> None:
        """
        Open a lobby message for players to join, and transition into a game
        :param serverId: Id of server lobby is opened in
        :param lobbyMsg: Id of join lobby message
        :return: None
        """
        if type(serverId) == int:
            serverId = str(serverId)
        if type(lobbyMsg) == int:
            lobbyMsg = str(lobbyMsg)
        game = Game()
        self._lobbies[serverId][lobbyMsg] = game

    def transition_lobby(self, serverId: Union[int, str], lobbyMsg: Union[int, str]) -> None:
        """
        Transition from a lobby into a fully fledged game managed by the manager
        :param serverId: Id of server lobby is opened in
        :param lobbyMsg: Id of join lobby message
        :return: None
        """
        if self._lobbies.get(serverId):
            if self._lobbies.get(lobbyMsg):
                self.add_game(self._lobbies[serverId][lobbyMsg])
                self._lobbies[serverId].pop(lobbyMsg)
    
    def add_game(self, game: Game, serverId: Union[int, str], gameWindow: Union[int, str]) -> bool:
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
