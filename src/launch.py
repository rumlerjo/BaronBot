"""
Launch the bot.
@author John Rumler https://github.com/shaftboyardee
"""

import pyjion
import interactions
from bot import Bot

pyjion.config(pgc=False)
pyjion.enable()

fp = open("botkey.txt")
client = interactions.Client(token=fp.read())
fp.close()

bot = Bot(client)

client.start()