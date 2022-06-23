"""
Launch the bot.
@author John Rumler https://github.com/shaftboyardee
"""

import pyjion
import interactions
from bot import Bot
from pymongo.mongo_client import MongoClient

pyjion.config(pgc=False)
pyjion.enable()

passfile = open("mongoconnect.txt", "r")
database_client = MongoClient(passfile.read())
passfile.close()
database = database_client.BaronBot
playerdata = database.players

fp = open("botkey.txt")
client = interactions.Client(token=fp.read())
fp.close()

bot = Bot(client)

client.start()