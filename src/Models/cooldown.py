"""
Bot command cooldown class implementation
@author John Rumler https://github.com/rumlerjo
"""

from typing import Optional, Union

from interactions import Snowflake
from Utilities.enums import CooldownEnums
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
        self.start = start

class CooldownManager:
    """
    A simple wrapper to manage command cooldowns
    """
    def __init__(self) -> None:
        self.globalCooldowns = dict()
        self.guildCooldowns = dict()
    
    def set_cooldown(self, commandId: int, userId: Snowflake, timeout: int, 
    cType: int, guildId: Optional[Snowflake] = None) -> None:
        """
        Set a global or guild timeout for commands bound to a specific user.
        Limiting of a whole guild is not currently supported
        :param commandId: Enum of command
        :param userId: User ID of user to timeout
        :param timeout: Time in seconds to timeout user
        :param cType: Cooldown type according to CooldownEnums
        :guildId: Guild ID to timeout user
        :return: None
        """
        userId = str(userId)
        guildId = str(guildId)
        
        if cType == CooldownEnums.GLOBAL:
            self.globalCooldowns[str(commandId)] = {userId: CooldownTimer(timeout, time())}
        elif cType == CooldownEnums.GUILD:
            self.guildCooldowns[guildId] = {str(commandId): {userId: CooldownTimer(timeout, time())}}
        
    def _check_guild_cooldown(self, guildId: Snowflake, userId: Snowflake, commandId: int) \
    -> Optional[Union[bool, int]]:
        """
        Check if a user is on cooldown for a specific command in a guild
        :param userId: Integer or string representing user's unique Id
        :param guildId: Integer or string representing a guild's unique string
        :param commandId: Enumeration of command
        :return: Whether user is on cooldown or None and time left on cooldown or None
        """
        # snowflake auto represents as string, just being safe
        userId = str(userId)
        guildId = str(guildId)

        guildCooldowns: dict = self.guildCooldowns.get(guildId)
        if guildCooldowns and guildCooldowns != {} and guildCooldowns:
            commandCooldowns: dict = guildCooldowns.get(str(commandId))
            if commandCooldowns and commandCooldowns != {}:
                userCooldown: CooldownTimer = commandCooldowns.get(userId)
                if userCooldown:
                    timeLeft = int(round(time() - userCooldown.start))
                    return timeLeft < userCooldown.time, timeLeft
        return None, None
    
    def get_cooldown(self, userId: Snowflake, commandId: int, guildId: Snowflake = None) -> Optional[int]:
        """
        Check if a user is on cooldown for a specific command
        :param userId: Integer or string representing user's unique Id
        :param commandId: Enumeration of command
        :param guildId: Integer or string representing a guild's unique string
        :return: Time left on cooldown or None
        """
        userId = str(userId)
        if guildId:
            guildId = str(guildId)
        # check for a guild cooldown
        if guildId:
            onCooldown, timeLeft = self._check_guild_cooldown(guildId, userId, commandId)
            if onCooldown:
                return timeLeft
            return None
        
        # check the global cooldowns
        commandCooldowns: dict = self.globalCooldowns.get(str(commandId))
        if commandCooldowns and commandCooldowns != {}:
            userCooldown: CooldownTimer = commandCooldowns.get(userId)
            if userCooldown:
                timeLeft = int(round(time() - userCooldown.start))
                onCooldown = timeLeft < userCooldown.time
                if onCooldown:
                    return timeLeft
                return None
