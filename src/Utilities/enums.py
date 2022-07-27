"""
Enumerations for various bot functions
@author John Rumler https://github.com/rumlerjo
"""

from enum import Enum

class CooldownEnums(Enum):
    """Enumerations of cooldown types"""
    GUILD = 1
    GLOBAL = 2

class CommandEnums(Enum):
    """Enumerations of commands"""
    PING = 1
    RELOAD = 2
    START = 3