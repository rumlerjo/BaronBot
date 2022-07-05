from interactions import Snowflake
from typing import Dict, List, Union
from game import Game
from settings import Settings

class GameManager:
    """A container to manage games"""
    def __init__(self) -> None:
        self._games = Dict[str, Dict[str, Game]]
        self._lobbies = Dict[str, Dict[str, Game]]

    def open_lobby(self, serverId: Snowflake, lobbyMsg: Snowflake, settings: Settings) -> Game:
        """
        Open a lobby message for players to join, and transition into a game
        :param serverId: Id of server lobby is opened in
        :param lobbyMsg: Id of join lobby message
        :return: None
        """
        serverId = str(serverId)
        lobbyMsg = str(lobbyMsg)
        game = Game()
        self._lobbies[serverId][lobbyMsg] = game
        return game

    def transition_lobby(self, serverId: Snowflake, lobbyMsg: Snowflake) -> None:
        """
        Transition from a lobby into a fully fledged game managed by the manager
        :param serverId: Id of server lobby is opened in
        :param lobbyMsg: Id of join lobby message
        :return: None
        """
        if self._lobbies.get(serverId):
            if self._lobbies[serverId].get(lobbyMsg):
                self.add_game(self._lobbies[serverId][lobbyMsg])
                self._lobbies[serverId].pop(lobbyMsg)
    
    def add_game(self, game: Game, serverId: Snowflake, gameWindow: Snowflake) -> bool:
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

    def get_game(self, serverId: Snowflake, gameWindow: Snowflake) -> Game:
        """
        Get a game from the manager
        :param serverId: A representation of the server the game is played in
        :param gameWindow: A representation of the main window the game is played in
        """
        if self._games.get(serverId):
            if self._games[serverId].get(gameWindow):
                return self._games[serverId][gameWindow]
