from typing import Optional
from Utilities.enums import COOLDOWN_ENUMS
from time import time

class CooldownTimer:
    """
    Simple wrapper for holding cooldown time information
    """
    def __init__(self, time: int, start: float) -> None:
        """
        :param time: Cooldown time in seconds
        :param start: Time at which cooldown began
        :return: None
        """
        self.time = time

class CooldownManager:
    """
    A simple wrapper to manage command cooldowns
    """
    def __init__(self) -> None:
        self.globalCooldowns = dict()
        self.guildCooldowns = dict()
    
    def set_cooldown(self, commandId: int, userId: str | int, time: int, 
    cType: int, guildId: Optional[str | int] = None) -> None:
        """
        Set a global or guild timeout for commands bound to a specific user.
        Limiting of a whole guild is not currently supported
        :param commandId: Enum of command
        :param userId: User ID of user to timeout
        :param time: Time in seconds to timeout user
        :param cType: Cooldown type according to CooldownEnums
        :guildId: Guild ID to timeout user
        :return: None
        """
        if type(userId) == int:
            userId = str(userId)
        if guildId and type(guildId) == int:
            guildId = str(guildId)
        
        if cType == COOLDOWN_ENUMS.GLOBAL:
            self.globalCooldowns[str(commandId)] = {userId: CooldownTimer(time, time.time())}
        elif cType == COOLDOWN_ENUMS.GUILD:
            self.guildCooldowns[guildId] = {str(commandId): {userId: CooldownTimer(time, time.time())}}
        
    def _check_guild_cooldown(self, guildId: str | int, userId: str | int) -> float | None:
        pass

