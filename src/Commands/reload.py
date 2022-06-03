from interactions import CommandContext, Extension, Client, OptionType, extension_command, Option
from bot import Bot

class Reload(Extension):
    def __init__(self, client: Client, parent: Bot) -> None:
        self.client = client
        self.parent = parent

    @extension_command(
        name = "reload", 
        description = "Reload currently active commands 🔄",
        scope = 351497847750787084,
        options = [
            Option(
                type = OptionType.BOOLEAN,
                name = "rebuild",
                description = "Rebuild all commands from scratch",
                required = False
            )
        ]
    )
    async def reload(self, ctx: CommandContext, rebuild: bool = False) -> None:
        await self.parent.reload_commands(rebuild)
        await ctx.send("Reloaded.", ephemeral=True)


    def __str__(self) -> str:
        return "Reload command: reloads all currently active commands."

    def __repr__(self) -> str:
        return str(self)