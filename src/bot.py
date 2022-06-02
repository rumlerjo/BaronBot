import interactions
from os import scandir
from importlib import import_module
from importlib.util import resolve_name
from typing import TypeVar, Set, Union
from Models.cooldown import CooldownManager
from interactions import Extension

# A generic class
T = TypeVar("T")
# Forward declaration of Bot
Bot = TypeVar("Bot")

from interactions import Extension

def get_commands(commands: set = set()) -> Set[T]:
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
        self.client = client
        self.cooldowns = CooldownManager()
        self.commands = set()
        self.extensions: Set[Extension] = set()
        self.load_commands()

    def load_commands(self) -> None:
        """
        Load commands onto the client
        :return: None
        """
        self.commands = get_commands(self.commands)
        for command in self.commands:
            self.extensions.add(command(self.client))
    
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
        for extension in self.extensions:
            extension.teardown()
        self.extensions = set()
        self.commands = set()
    
    def set_cooldown(self, command_name: str, type: int = 1):
        pass


    