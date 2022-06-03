from interactions import Extension, Client
from bot import Bot

class Ping(Extension):
    def __init__(self, client: Client, parent: Bot) -> None:
        self.i = "hachi"
        self.client = client
        self.parent = parent

    def __str__(self) -> str:
        return "Ping command: sends a user the current bot latency."

    def __repr__(self) -> str:
        return str(self)