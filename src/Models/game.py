from typing import TypeVar, List

Player = TypeVar("Player")

class Game:
    def __init__(self, players: List[str], guild: str, gameWindow: str | int) -> None:
        self._players = dict() # format will be "userid" : player object
        self._guildId = guild
        self._roads = dict() # in format "road name": owner player object
        self._gameWindow = str(gameWindow) # the main message window
