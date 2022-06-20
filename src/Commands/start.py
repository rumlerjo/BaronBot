from tkinter.ttk import Style
from tracemalloc import start
from interactions import ButtonStyle, CommandContext, ComponentContext, \
Extension, Client, OptionType, extension_command, Option, Button, ComponentType, extension_component
from bot import Bot



class Start(Extension):
    startButton = Button(
            style = ButtonStyle.PRIMARY,
            label = "Start!",
            custom_id = "StartButton"
        )
    
    def __init__(self, client: Client) -> None:
        self.client = client
        self._parent: Bot = None

    @extension_command(
        name = "start",
        description = "Start a game lobby.",
        scope = 351497847750787084,
        options = [
            Option (
                name = "max_players",
                description = "The maximum number of players between 3 and 6 for this game.",
                type = OptionType.INTEGER,
                max_value = 6,
                min_value = 3
            )
        ]
    )
    async def start(self, ctx: CommandContext, max_players: int = 6):
        # once game manager is a thing check to see
        # if player already is in a game for that
        # server
        await ctx.send("Start", components = self.startButton,
        ephemeral = True)

    @extension_component(startButton)
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