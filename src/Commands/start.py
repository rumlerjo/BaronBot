from typing import Union
from interactions import ButtonStyle, Color, CommandContext, ComponentContext, Embed, \
Extension, Client, OptionType, SelectMenu, Snowflake, extension_command, Option, Button, ComponentType, \
    extension_component, SelectOption, ActionRow
from Models.settings import Settings
from bot import Bot
from Utilities.enums import CommandEnums, CooldownEnums

# create settings and pass to game obj
settings_tracker = {}

def make_embed(settings: Settings, ctx: Union[CommandContext, ComponentContext]) -> Embed:
        settings_embed = Embed()
        settings_embed.color = Color().green
        settings_embed.title = "Settings"
        settings_embed.add_field(name="Maximum players", value=f"{settings.maxPlayers} Players")
        settings_embed.add_field(name="Balanced PA Railroad", 
        value="Enabled" if settings.balancedPa else "Disabled")
        settings_embed.add_field(name="Pay Per Move on Unowned Road", 
        value="Enabled" if settings.payPerMove else "Disabled")
        settings_embed.add_field(name="Pay on Owned Roads",
        value="Enabled" if settings.payOnOwnedRoads else "Disabled")
        settings_embed.set_footer(text="Interactions available for " +
        ctx.user.username + "#" + ctx.user.discriminator, icon_url=ctx.user.avatar_url)
        return settings_embed

settings_buttons = [
    ActionRow (
        components = [
            SelectMenu (
                placeholder = "Max Players",
                options = [
                    SelectOption (
                        label = f"{i} Players",
                        value = i,
                        default = True if i == 3 else False
                    ) for i in range(3,7)
                ],
                custom_id = "PlayerSelect"
            ),
        ]
    ),
    ActionRow (
        components = [
            Button (
                style = ButtonStyle.SECONDARY,
                label = "Balanced PA",
                custom_id = "BPA"
            ),
            Button (
                style = ButtonStyle.SECONDARY,
                label = "Pay Per Move",
                custom_id = "PPM"
            ),
            Button (
                style = ButtonStyle.SECONDARY, 
                label = "Pay on Owned",
                custom_id = "POOR"
            ),
            Button (
                style = ButtonStyle.SUCCESS,
                label = "Start!",
                custom_id = "OpenLobby"
            ),
        ]
    )
]

class Start(Extension):
    def __init__(self, client: Client) -> None:
        self.client = client
        self._parent: Bot = None

    @extension_command (
        name = "start",
        description = "Start a game lobby.",
        scope = 351497847750787084
    )
    async def start(self, ctx: CommandContext, maxPlayers: int = 6):
        # once game manager is a thing check to see
        # if player already is in a game for that
        # server
        cooldown = self._parent.get_cooldown(ctx.user.id, CommandEnums.START, ctx.guild_id)
        if cooldown:
            await ctx.send("You are on cooldown for this command for another " + str(cooldown) + " seconds.",
            ephemeral = True)
            return
        settings = Settings(ctx.user.id)
        msg = await ctx.send(components=settings_buttons, embeds=make_embed(settings, ctx))
        settings_tracker[msg.id] = settings
        self._parent.set_cooldown(CooldownEnums.GUILD, CommandEnums.START, ctx.user.id,
        10, ctx.guild_id)

        
    @extension_component("PlayerSelect")
    async def toggle_bpa(self, ctx: ComponentContext, value: int) -> None:
        settings: Settings = settings_tracker.get(ctx.message.id)
        if settings.userId != ctx.user.id:
            await ctx.send("These interactions aren't available for you.", ephemeral=True)
            return
        settings.maxPlayers = value
        # ctx.edit as opposed to ctx.message.edit so interaction is responded to
        await ctx.edit(embeds=make_embed(settings, ctx))

    @extension_component("BPA")
    async def toggle_bpa(self, ctx: ComponentContext) -> None:
        print("bpa")
        settings: Settings = settings_tracker.get(ctx.message.id)
        if settings.userId != ctx.user.id:
            await ctx.send("These interactions aren't available for you.", ephemeral=True)
            return
        settings.balancedPa = not settings.balancedPa
        # ctx.edit as opposed to ctx.message.edit so interaction is responded to
        await ctx.edit(embeds=make_embed(settings, ctx))
        
    @extension_component("PPM")
    async def toggle_bpa(self, ctx: ComponentContext) -> None:
        settings: Settings = settings_tracker.get(ctx.message.id)
        if settings.userId != ctx.user.id:
            await ctx.send("These interactions aren't available for you.", ephemeral=True)
            return
        settings.payPerMove = not settings.payPerMove
        # ctx.edit as opposed to ctx.message.edit so interaction is responded to
        await ctx.edit(embeds=make_embed(settings, ctx))
        
    @extension_component("POOR")
    async def toggle_bpa(self, ctx: ComponentContext) -> None:
        settings: Settings = settings_tracker.get(ctx.message.id)
        if settings.userId != ctx.user.id:
            await ctx.send("These interactions aren't available for you.", ephemeral=True)
            return
        settings.payOnOwnedRoads = not settings.payOnOwnedRoads
        # ctx.edit as opposed to ctx.message.edit so interaction is responded to
        await ctx.edit(embeds=make_embed(settings, ctx))

    @extension_component("OpenLobby")
    async def start_response(self, ctx: ComponentContext) -> None:
        await ctx.send("Hi!!")
        
    def add_parent(self, parent: Bot) -> None:
        self._parent = parent
    
    def __str__(self) -> str:
        return "Start: Starts creation of a game."

    def __repr__(self) -> str:
        return str(self)
    

def setup(client: Client):
    return Start(client)