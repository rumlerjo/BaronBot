import interactions
from os import scandir
from typing import TypeVar, Set, Optional, Union
from Models.cooldown import CooldownManager
from interactions import Extension, Snowflake
from interactions.api.dispatch import Listener

# A generic class
T = TypeVar("T")
# Forward declaration of Bot
Bot = TypeVar("Bot")

class BotExtension(Extension):
    """
    A template class used for typehinting
    """
    def add_parent(self, parent: Bot) -> None:
        pass

def get_command_paths() -> Set[T]:
    """
    Gets all names of extensions to load onto the client
    :return: Set of all extension names
    """
    paths = set()
    for file in scandir("./src/Commands"):
        if file.is_file and file.name.find(".py") != -1:
            command_name = file.name.replace(".py", "")
            paths.add(f"Commands.{command_name}")
    return paths

class Bot:
    """
    Wrapper for the bot and some of its functions.
    """
    def __init__(self, client: interactions.Client) -> None:
        self._client = client
        self._cooldowns = CooldownManager()
        self._listener = Listener() # probably not necessary for the time being
        # get the event listener running on the same loop as the bot
        self._listener.loop = self._client._loop
        # used as a checker to see which commands are running
        self._extensions: Set[Extension] = set()
        self.load_commands()

    def load_commands(self) -> None:
        """
        Load commands onto the client
        :return: None
        """
        for command in get_command_paths():
            extension: BotExtension = self._client.load(command)
            self._extensions.add(extension)
            extension.add_parent(self)

    # fixedish
    async def reload_commands(self) -> None:
        """
        Reload commands on the client
        :return: None
        """
        for command in get_command_paths():
            extension: BotExtension = self._client.reload(command)
            self._extensions.add(extension)
            extension.add_parent(self)

    async def unload_all_commands(self) -> None:
        """
        Unload all currently loaded commands
        :return None:
        """
        for command in get_command_paths():
            self._client.remove(command)
        # just set it back to empty because it (should) be
        self._extensions = set()

    async def unload_and_reload_commands(self) -> None:
        """
        Fully unload and reload every currently loaded extension
        :return None:
        """
        self.unload_all_commands()
        self.load_commands()
        
    def set_cooldown(self, cType: int, commandId: int, userId: Union[str, int], 
    time: int, guildId: Optional[Union[str, int]] = None) -> None:
        """
        A wrapper for CooldownManager's set_cooldown
        :param cType: Enumeration of cooldown type
        :param commandId: Command enumeration
        :param userId: Integer or String representation of a user's unique identifier
        :param time: Amound of time in seconds to timeout command
        :param guildId: Integer or String representation of a guild's unique identifier
        :return: None
        """
        self._cooldowns.set_cooldown(commandId, userId, time, cType, guildId)

    def get_cooldown(self, userId: Snowflake, commandId: int, 
    guildId: Optional[Snowflake] = None) -> Optional[int]:
        """
        A wrapper for CooldownManager's get_cooldown
        :param userId: Integer or String representation of a user's unique identifier
        :param commandId: Command enumeration
        :param guildId: Integer or String representation of a guild's unique identifier
        :return: Amount of time left in cooldown or None
        """
        return self._cooldowns.get_cooldown(userId, commandId, guildId)
    