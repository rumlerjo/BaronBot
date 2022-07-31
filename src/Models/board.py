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
# TODO: Create a setter for pixel coordinates in Space instead of 
# initializer AND an excel spreadsheet of all the coordinates

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

def make_spaces() -> Dict[str, Space]:
    # Atchison, Topeka, & Santa Fe
    cities = {1: "San Francisco/Oakland", 47: "Houston", 42: "Fort Worth", 39: "Oklahoma City", 16: "Phoenix", 
            24: "El Paso", 36: "Kansas City", 60: "Chicago", 29: "Pueblo", 8: "Los Angeles", 10: "San Diego"}
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
    cities = {2: "Salt Lake City", 9: "Denver", 11: "Pueblo"}
    dr = create_road_spaces(RAILROADS["D&RGW"], cities, "DR", 13)

    # Great Northern
    cities = {1: "Portland OR", 5: "Spokane", 8: "Seattle", 24: "Fargo", 27: "Minneapolis/St. Paul", 30: "Butte"}
    gn = create_road_spaces(RAILROADS["GN"], cities, "GN", 34)

    # Gulf, Mobile, & Ohio
    cities = {1: "Kansas City", 7: "Chicago", 8: "St. Louis", 18: "Mobile"}
    gm = create_road_spaces(RAILROADS["GM&O"], cities, "GM", 18)

    # Illinois Central
    cities = {1: "New Orleans", 9: "Shreveport", 12: "Memphis", 18: "Louisville", 20: "St. Louis", 25: "Chicago"}
    ic = create_road_spaces(RAILROADS["IC"], cities, "IC", 25)

    # Louisville & Nashville
    cities = {1: "New Orleans", 3: "Mobile", 10: "Birmingham", 13: "Nashville", 16: "Memphis", 20: "Louisville", 
            21: "Cincinatti", 25: "Knoxville", 28: "Atlanta", 29: "Chattanooga"}
    ln = create_road_spaces(RAILROADS["L&N"], cities, "LN", 30)

    # Missouri Pacific
    cities = {1: "San Antonio", 7: "Houston", 11: "Little Rock", 13: "Memphis", 17: "St. Louis", 23: "Kansas City",
            34: "Pueblo"}
    mp = create_road_spaces(RAILROADS["MP"], cities, "mp", 34)

    # New York Central
    cities = {1: "Chicago", 5: "Detroit", 6: "Cleveland", 8: "Buffalo", 11: "Albany", 13: "New York", 19: "St. Louis", 
            21: "Cincinatti"}
    ny = create_road_spaces(RAILROADS["NYC"], cities, "NY", 21)

    # New York, New Haven, & Hartford
    cities = {1: "New York", 4: "Boston"}
    nh = create_road_spaces(RAILROADS["NYNH&H"], cities, "NH", 4)

    # Norfolk & Western
    cities = {4: "Columbus", 13: "Norfolk"}
    nw = create_road_spaces(RAILROADS["N&W"], cities, "NW", 13)

    # Northern Pacific
    # add +1 to all bc missed portland oregon
    cities = {1: "Portland OR", 3: "Seattle", 7: "Spokane", 12: "Butte", 15: "Billings", 24: "Fargo", 27: "Minneapolis/St. Paul"}
    np = create_road_spaces(RAILROADS["NP"], cities, "NP", 27)

    # Pennsylvania
    cities = {1: "St. Louis", 4: "Indianapolis", 6: "Chicago", 10: "Cincinatti", 11: "Columbus", 13: "Pittsburgh", 
            16: "Cleveland", 18: "Buffalo", 22: "Baltimore", 23: "Washington", 24: "Philadelphia", 26: "New York"}
    pa = create_road_spaces(RAILROADS["PA"], cities, "PA", 26)

    # Richmond, Fredericksburg, & Potomac
    cities = {1: "Washington", 3: "Richmond"}
    rf = create_road_spaces(RAILROADS["RF&P"], cities, "RF", 3)

    # Seaboard Airline
    # messed up this one too, from 14 above JAX onward +1
    cities = {7: "Jacksonville", 13: "Miami", 14: "Tampa", 17: "Charleston", 22: "Charlotte", 25: "Atlanta", 
            28: "Birmingham", 33: "Richmond"}
    sa = create_road_spaces(RAILROADS["SAL"], cities, "SA", 33)

    # Southern Pacific
    cities = {1: "Portland OR", 8: "Sacramento", 10: "San Francisco/Oakland", 16: "Los Angeles", 21: "Phoenix",
            26: "El Paso", 32: "San Antonio", 39: "New Orleans", 42: "Shreveport", 46: "Tucumcari",
            48: "Reno"}
    sp = create_road_spaces(RAILROADS["SP"], cities, "SP", 53)

    # Southern Railway
    cities = {1: "New Orleans", 6: "Birmingham", 9: "Memphis", 12: "Chattanooga", 14: "Atlanta", 17: "Knoxville",
            23: "Charlotte", 29: "Washington"}
    so = create_road_spaces(RAILROADS["SOU"], cities, "SO", 29)

    # St. Louis - San Francisco
    cities = {1: "Fort Worth", 2: "Dallas", 10: "Oklahoma City", 14: "Kansas City", 17: "St. Louis", 21: "Memphis",
            24: "Birmingham"}
    sl = create_road_spaces(RAILROADS["SLSF"], cities, "SL", 24)

    # Texas & Pacific
    cities = {1: "El Paso", 8: "Fort Worth", 9: "Dallas", 12: "Shreveport", 17: "New Orleans"}
    tp = create_road_spaces(RAILROADS["T&P"], cities, "TP", 17)

    # Union Pacific
    # Messed up Denver will be on 44
    # LA is 43
    cities = {1: "Portland OR", 10: "Pocatello", 14: "Butte", 29: "Omaha", 33: "Kansas City", 34: "Salt Lake City",
    39: "Las Vegas", 43: "Los Angeles", 44: "Denver"}
    up = create_road_spaces(RAILROADS["UP"], cities, "UP", 44)

    # Western Pacific
    # Messed up this one reno is 8 one above reno is 7 on and on
    cities = {1: "San Francisco/Oakland", 3: "Sacramento", 8: "Reno", 13: "Salt Lake City"}
    wp = create_road_spaces(RAILROADS["WP"], cities, "WP", 13)
    
    return {**at, **ac, **bo, **bm, **co, **cn, **cb, **cr, **cm, **dr, **gn, **gm, **ic, **ln, **mp, **ny, **nh, 
            **nw, **np, **pa, **rf, **sa, **sp, **so, **sl, **tp, **up, **wp}
    
def make_connections() -> AdjacencyGraph:
    connection_map = {
        "SP1": ["UP1", "SP2", "GN1", "NP1"],
        "SP2": ["SP1", "GN1", "UP1", "SP3"],
        "SP3": ["SP2", "SP4"],
        "SP4": ["SP3", "SP5"],
        "SP5": ["SP4", "SP6"],
        "SP6": ["SP5", "SP7"],
        "SP7": ["SP6", "SP8"],
        "SP8": ["WP3", "WP4", "SP47", "WP2"]
    }
    spaces = make_spaces()
    graph = AdjacencyGraph()
    for key, connections in connection_map.items():
        for connection in connections:
            graph.add_nodeless_adjacency(key, connection, spaces[key], spaces[connection])
            
    return graph


DEFAULT_GRAPH = make_connections()

BALANCED_GRAPH = DEFAULT_GRAPH.copy()

class Board:
    """
    A class to represent the board the game is played on
    """
    __slots__ = ["graph"]

    def __init__(self) -> None:
        pass
