"""
Rail Baron board setup
@author John Rumler https://github.com/rumlerjo
"""

from Models.player import Player
from Models.railroad import Road
from Utilities.adjacencygraph import AdjacencyGraph
from typing import Dict, Optional, Tuple

ROAD_NAMES = ['Atchison, Topeka, & Santa Fe', 'Atlantic Coast Line', 'Baltimore & Ohio', 
'Boston & Maine', 'Chesapeake & Ohio', 'Chicago & Northwestern', 'Chicago, Burlington, & Quincy', 
'Chicago, Rock Island, & Pacific', 'Chicago, Milwaukee, St. Paul, & Pacific', 'Denver & Rio Grande Western', 
'Great Northern', 'Gulf, Mobile, & Ohio', 'Illinois Central', 'Louisville & Nashville', 'Missouri Pacific', 
'New York Central', 'New York, New Haven, & Hartford', 'Norfolk & Western', 'Northern Pacific', 'Pennsylvania', 
'Richmond, Fredericksburg, & Potomac', 'Seaboard Airline', 'Southern Pacific', 'Southern Railway', 
'St. Louis - San Francisco', 'Texas & Pacific', 'Union Pacific', 'Western Pacific']

ROAD_ABVS = ["AT&SF", "ACL", "B&O", "B&M", "C&O", "C&NW", "CB&Q", "CRI&P", "CMStP&P", "D&RGW", "GN",
"GM&O", "IC", "L&N", "MP", "NYC", "NYNH&H", "N&W", "NP", "PA", "RF&P", "SAL", "SP", "SOU",
"SLSF", "T&P", "UP", "WP"]

ROAD_PRICES = [40000, 12000, 24000, 4000, 20000, 14000, 20000, 29000, 18000, 6000, 17000,
12000, 14000, 18000, 21000, 28000, 4000, 12000, 14000, 30000, 4000, 14000, 42000, 20000,
19000, 10000, 40000, 8000]

# generator for dictionary
RAILROADS = {ROAD_ABVS[i]: Road(ROAD_NAMES[i], ROAD_ABVS[i], ROAD_PRICES[i]) for i in range(len(ROAD_NAMES))}

class Space:
    """
    A class to represent a space that a piece can be on
    """
    # maybe i should consistently do this lol
    __slots__ = ["road", "position", "occupiedBy", "pxCoordinates"]
    
    def __init__(self, road: Road, name: str, pxCoordinates: Tuple[int, int] = (0, 0)) -> None:
        """
        :param road: Railroad that the space is a part of
        :param name: string code of space
        :param region: Region abbreviation in string form
        :param pxCoordinates: Pixel coordinates of space in board image
        :return: None
        """
        self.road = road
        self.position = name
        self.occupiedBy: Player = None
        self.pxCoordinates = pxCoordinates # the coordinates in board image of the space
        # getters and setters or just directly . index it? I think the latter
        
    def __str__(self) -> str:
        return "Space " + self.position + " of " + self.road.name()
    
    def __repr__(self) -> str:
        return str(self)

class CitySpace(Space):
    """
    A subclass of space allowing for a city to reside on the space\n
    Useful for origin and destination tracking
    """
    __slots__ = ["city"]

    def __init__(self, road: Road, name: str, pxCoordinates: Tuple[int, int] = (0, 0), 
    city: Optional[str] = None) -> None:
        super().__init__(road, name, pxCoordinates)
        self.city: str = city
    
    def __str__(self) -> str:
        return "City " + self.city + " on " + self.road.name()


# define all the spaces first before adding them as edges in the graph
# left to right for the most part
# TODO: Finish drawn map and pixel coordinates

def create_road_spaces(railroad: Road, cities: Dict[int, str], abv: str, spaces: int) -> Dict[str, Space]:
    """
    Create a dictionary of spaces on a given railroad
    :param railroad: Railroad the spaces are a part of
    :param cities: The cities on the railroad and their corresponding
    number code from Assets/Images/Coded Board
    :param: The coded abbreviation from Assets/Images/Coded Board
    :return: A Dictionary of form key/pair str/Space
    """
    return {f"{abv}{i}": (Space(railroad, f"{abv}{i}") if not cities.get(i) else 
    CitySpace(railroad, f"{abv}{i}", city = cities.get(i))) for i in range(1, spaces + 1)}

# Atchison, Topeka, & Santa Fe
cities = {1: "San Francisco/Oakland", 47: "Houston", 42: "Fort Worth", 39: "Oklahoma City", 
16: "Phoenix", 24: "El Paso", 36: "Kansas City", 60: "Chicago", 29: "Pueblo", 8: "Los Angeles", 10: "San Diego"}
at = create_road_spaces(RAILROADS["AT&SF"], cities, "AT", 60)

# Atlantic Coast Line
cities = {1: "Birmingham", 4: "Atlanta", 13: "Charleston", 20: "Richmond", 23: "Jacksonville", 25: "Tampa"}
ac = create_road_spaces(RAILROADS["ACL"], cities, "AC", 25)

# Baltimore & Ohio
cities = {1: "St. Louis", 5: "Cincinatti", 12: "Pittsburgh", 15: "Chicago", 20: "Washington", 21: "Baltimore", 
22: "Philadelphia", 24: "New York"} # exclude 22-24 when connecting original board, these are for balancing
bo = create_road_spaces(RAILROADS["B&O"], cities, "BO", 24)

# Boston & Maine
cities = {1: "Albany", 4: "Portland ME", 5: "Boston"}
bm = create_road_spaces(RAILROADS["B&M"], cities, "BM", 5)

# Chesapeake & Ohio
cities = {1: "Chicago", 4: "Cincinatti", 9: "Louisville", 14: "Richmond", 16: "Washington", 21: "Detroit", # can't have shit
24: "Buffalo"}
co = create_road_spaces(RAILROADS["C&O"], cities, "CO", 24)

# Chicago & Northwestern
cities = {1: "Casper", 5: "Rapid City", 12: "Minneapolis/St. Paul", 17: "Omaha", 25: "Chicago", 27: "Milwaukee"}
cn = create_road_spaces(RAILROADS["C&NW"], cities, "CN", 30)

# Chicago, Burlington, & Quincy
cities = {1: "Billings", 5: "Casper", 9: "Denver", 11: "Pueblo", 20: "Fort Worth", 27: "Omaha", 33: "Chicago", 
42: "Kansas City", 45: "St. Louis"}
cb = create_road_spaces(RAILROADS["CB&Q"], cities, "CB", 45)

# Chicago, Rock Island, & Pacific
# This one got SNAFU'd on the pic (wb file SNAFU'd too) - unlabelled leading to Chicago
# are 45 46 47 48
cities = {1: "Tucumcari", 9: "Kansas City", 12: "Des Moines", 18: "Omaha", 16: "Minneapolis/St. Paul",
32: "Oklahoma City", 38: "Fort Worth", 42: "Little Rock", 44: "Memphis", 48: "Chicago"}
cr = create_road_spaces(RAILROADS["CRI&P"], cities, "CR", 48)

# Chicago, Milwaukee, St. Paul, & Pacific
cities = {1: "Seattle", 4: "Spokane", 21: "Minneapolis/St. Paul", 25: "Milwaukee", 27: "Chicago"}
cm = create_road_spaces(RAILROADS["CMStP&P"], cities, "CM", 27)

# Denver & Rio Grande Western
cities = {2: "Salt Lake City", }

# Great Northern
cities = {1: "Portland OR", 5: "Spokane", 8: "Seattle", 24: "Fargo", 27: "Minneapolis/St. Paul", 30: "Butte"}
gn = create_road_spaces(RAILROADS["GN"], cities, "GN", 34)

# Union Pacific
cities = {1: "Portland OR", 10: "Pocatello", 14: "Butte", 29: "Omaha", 33: "Kansas City", 34: "Denver",
39: "Las Vegas", 43: "Los Angeles"}
up = create_road_spaces(RAILROADS["UP"], cities, "UP", 43)

DEFAULT_GRAPH = AdjacencyGraph()

BALANCED_GRAPH = DEFAULT_GRAPH.copy()

class Board:
    """
    A class to represent the board the game is played on
    """
    __slots__ = ["graph"]

    def __init__(self) -> None:
        pass