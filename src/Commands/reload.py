from interactions import CommandContext, Extension, Client, OptionType, extension_command, Option
from bot import Bot

# will need to lock down to only me being able to use this

class Reload(Extension):
    def __init__(self, client: Client) -> None:
        self.client = client
        self._parent: Bot = None

    @extension_command(
        name = "reload", 
        description = "Reload currently active commands 🔄 (Dev Tool)",
        scope = 351497847750787084
    )
    async def reload(self, ctx: CommandContext) -> None:
        if ctx.user.id != "311663246622982145":
            await ctx.send("Additional permissions are required: `developer`.")
        await self._parent.reload_commands()
        await ctx.send("Reloaded.", ephemeral=True)
    
    def add_parent(self, parent: Bot) -> None:
        self._parent = parent

    def __str__(self) -> str:
        return "Reload command: reloads all currently active commands."

    def __repr__(self) -> str:
        return str(self)

def setup(client: Client):
    return Reload(client)