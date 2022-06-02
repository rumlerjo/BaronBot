class CooldownEnums:
    """Enumerations of cooldown types"""
    def __init__(self) -> None:
        self.GUILD = 1
        self.GLOBAL = 2

COOLDOWN_ENUMS = CooldownEnums()

class CommandEnums:
    """Enumerations of commands"""
    def __init__(self) -> None:
        self.PING = 1
    
COMMAND_ENUMS = CommandEnums()