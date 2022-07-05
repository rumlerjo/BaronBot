from typing import TypeVar, List, Union, Optional
from railroad import Road
from interactions import Snowflake, User
from settings import Settings
from player import Player

names = ['Atchison, Topeka, & Santa Fe', 'Atlantic Coast Line', 'Baltimore & Ohio', 
'Boston & Maine', 'Chesapeake & Ohio', 'Chicago & Northwestern', 'Chicago, Burlington, & Quincy', 
'Chicago, Rock Island, & Pacific', 'Chicago, Milwaukee, St. Paul, & Pacific', 'Denver & Rio Grande Western', 
'Great Northern', 'Gulf, Mobile, & Ohio', 'Illinois Central', 'Louisville & Nashville', 'Missouri Pacific', 
'New York Central', 'New York, New Haven, & Hartford', 'Norfolk & Western', 'Northern Pacific', 'Pennsylvania', 
'Richmond, Fredericksburg, & Potomac', 'Seaboard Airline', 'Southern Pacific', 'Southern Railway', 
'St. Louis - San Francisco', 'Texas & Pacific', 'Union Pacific', 'Western Pacific']

abvs = ["AT&SF", "ACL", "B&O", "B&M", "C&O", "C&NW", "CB&Q", "CRI&P", "CMStP&P", "D&RGW", "GN",
"GM&O", "IC", "L&N", "MP", "NYC", "NYNH&H", "N&W", "NP", "PA", "RF&P", "SAL", "SP", "SOU",
"SLSF", "T&P", "UP", "WP"]

prices = [40000, 12000, 24000, 4000, 20000, 14000, 20000, 29000, 18000, 6000, 17000,
12000, 14000, 18000, 21000, 28000, 4000, 12000, 14000, 30000, 4000, 14000, 42000, 20000,
19000, 10000, 40000, 8000]

class Game:
    def __init__(self, guild: Snowflake, settings: Settings, gameWindow: Union[int, str]) -> None:
        self._players: List[Player] = list()
        self._guildId = guild
        self._roads = [Road(names[i], abvs[i], prices[i]) for i in range(len(names))]
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



