import interactions
from os import scandir
from importlib import import_module
from importlib.util import resolve_name
from typing import TypeVar, Set, Union, Optional
from Models.cooldown import CooldownManager
from interactions import Extension

# A generic class
T = TypeVar("T")
# Forward declaration of Bot
Bot = TypeVar("Bot")

from interactions import Extension

def get_commands() -> Set[T]:
    """
    Load all extensions in a more specific way than included in
    the interactions wrapper.
    :return: Set of all extensions
    """
    commands = set()
    for file in scandir("./src/Commands"):
        if file.is_file and file.name.find(".py") != -1:
            command_name = file.name.replace(".py", "")
            name = resolve_name(f"Commands.{command_name}", None)
            module = import_module(name)
            commands.add(getattr(module, command_name.capitalize()))
    return commands

class Bot:
    """
    Wrapper for the bot and some of its functions.
    """
    def __init__(self, client: interactions.Client) -> None:
        self._client = client
        self._cooldowns = CooldownManager()
        # used as a checker to see which commands are running
        self._currently_running = set()
        self._extensions: Set[Extension] = set()
        self.load_commands()

    def load_commands(self) -> None:
        """
        Load commands onto the client
        :return: None
        """
        for command in get_commands():
            if command not in self._currently_running:
                self._currently_running.add(command)
                self._extensions.add(command(self.client, self))
    
    def reload_commands(self, rebuild = False) -> None:
        """
        Reload commands on the client
        :param rebuild: Rebuild commands and modules from scratch
        :return: None
        """
        if rebuild:
            self.unload_commands()
        self.load_commands()
    
    def unload_commands(self) -> None:
        """
        Destroy currently running commands
        :return: None
        """
        for extension in self._extensions:
            extension.teardown()
        self._extensions = set()
        self._currently_running = set()
    
    def set_cooldown(self, cType: int, commandId: int, userId: int | str, 
    time: int, guildId: Optional[str | int] = None) -> None:
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

    def get_cooldown(self, userId: str | int, commandId: int, 
    guildId: Optional[str | int] = None) -> int | None:
        """
        A wrapper for CooldownManager's get_cooldown
        :param userId: Integer or String representation of a user's unique identifier
        :param commandId: Command enumeration
        :param guildId: Integer or String representation of a guild's unique identifier
        :return: Amount of time left in cooldown or None
        """
        return self._cooldowns.get_cooldown(userId, commandId, guildId)
    