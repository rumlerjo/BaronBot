"""
Bot user class implementation
@author John Rumler https://github.com/rumlerjo
"""

from typing import Optional, List, Union
from interactions import Snowflake
from interactions.client import User

class BaronUser:
    """
    Bot user info
    """

    __slots__ = ["_wins", "_rating", "_playing_in", "_user_info"]

    def __init__(self, data: Optional[dict], discord_user: User) -> None:
        # TODO once saving (mongoDB??) add loading from a dict
        if not data:
            self._wins = 0 #games won
            self._rating = 0
        # keep track of what servers player is currently playing in.
        # would like to keep player from playing multiple games
        # in one server for the time being
        self._playing_in = List[Snowflake] # a list of servers player is currently in
        self._user_info = discord_user
    
    def __str__(self) -> str:
        return "Player object for: " + self._user_info.username
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, user_id: Union[str, int]) -> bool:
        return self._user_info.id == user_id
