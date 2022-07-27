"""
Game settings class implementation
@author John Rumler https://github.com/rumlerjo
"""

from interactions import Snowflake

class Settings:
    """
    A class representing game settings
    """
    def __init__(self, userId: Snowflake) -> None:
        self.balancedPa = False
        self.maxPlayers = 3
        self.payPerMove = False
        self.payOnOwnedRoads = False
        self.userId = userId # the user who opened the lobby