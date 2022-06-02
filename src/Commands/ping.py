from interactions import Extension

class Ping(Extension):
    def __init__(self, client) -> None:
        self.i = "hachi"
        self.client = client

    def __str__(self) -> str:
        return "Ping command: sends a user the current bot latency."

    def __repr__(self) -> str:
        return str(self)