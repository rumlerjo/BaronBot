from typing import TypeVar, List, Union

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

class Road:
    """Railroad Class"""
    def __init__(self, name: str, abv: str, price: int) -> None:
        self._owner: Player = None
        self._name = name
        self._abbreviation = abv
        self._price = price
        
    def __eq__(self, name: str) -> bool:
        return name.lower() == self._name.lower()

    def __str__(self) -> str:
        out = self._name + "\nPrice: " + str(self._price) + "\nOwned by: "
        if self._owner:
            out += self._owner.name + "\n"
        else:
            out += "Nobody\n"
        return out
    
    def __repr__(self) -> str:
        return str(self)


class Game:
    def __init__(self, players: List[Player], guild: str, gameWindow: Union[int, str]) -> None:
        self._players = dict() # format will be "userid" : player object
        self._guildId = guild
        self._roads = [Road(names[i], abvs[i], prices[i]) for i in range(len(names))] # in format "road name": owner player id
        self._gameWindow = str(gameWindow) # the main message window
    
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

game = Game(players = [], guild = "1", gameWindow = "2")

game.print_roads()


