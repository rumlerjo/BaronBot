from interactions import CommandContext, Extension, Client, extension_command
from bot import Bot
from Utilities.enums import CommandEnums, CooldownEnums

class Ping(Extension):
    def __init__(self, client: Client, parent: Bot) -> None:
        self.client = client
        self.parent = parent

    @extension_command(
        name="ping", 
        description="Get current bot latency 🏓",
        scope=351497847750787084
    )
    async def ping(self, ctx: CommandContext) -> None:
        enum = CommandEnums.PING
        cooldown = self.parent.get_cooldown(ctx.user.id, CommandEnums.PING)
        if cooldown:
            await ctx.send("You are on cooldown for Ping! Please wait " + str(cooldown) + " seconds.",
            ephemeral = True)
            return
        await ctx.send("Pong! " + str(round(self.client.latency)) + "ms response.")
        self.parent.set_cooldown(CooldownEnums.GLOBAL, enum, ctx.user.id, 5)

    def __str__(self) -> str:
        return "Ping command: sends a user the current bot latency."

    def __repr__(self) -> str:
        return str(self)