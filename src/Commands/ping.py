from interactions import CommandContext, Extension, Client, extension_command, Permissions
from bot import Bot
from Utilities.enums import CommandEnums, CooldownEnums

class Ping(Extension):
    def __init__(self, client: Client) -> None:
        self.client = client
        self._parent: Bot = None

    @extension_command (
        name = "ping", 
        description = "Get current bot latency 🏓",
        scope = 351497847750787084
    )
    async def ping(self, ctx: CommandContext) -> None:
        enum = CommandEnums.PING
        cooldown = self._parent.get_cooldown(ctx.user.id, enum)
        if cooldown:
            await ctx.send("You are on cooldown for this command for another " + str(cooldown) + " seconds.",
            ephemeral = True)
            return
        await ctx.send("Pong! " + str(round(self.client.latency)) + "ms response.")
        self._parent.set_cooldown(CooldownEnums.GLOBAL, enum, ctx.user.id, 5)
        
    def add_parent(self, parent: Bot) -> None:
        self._parent = parent

    def __str__(self) -> str:
        return "Ping command: sends a user the current bot latency."

    def __repr__(self) -> str:
        return str(self)

def setup(client: Client):
    return Ping(client)