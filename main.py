import mysql.connector
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from cogs.sentence import Sentence
from cogs.economy import Economy
from cogs.loger import Loger
from cogs.reactor import Reactor

load_dotenv(".env")

client = commands.Bot(command_prefix="$",intents=discord.Intents.all())
mydb = None;
mycursor = None;

@client.event
async def on_ready():
    global mydb
    global mycursor
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sentencebot")
    mycursor = mydb.cursor()
    await client.add_cog(Sentence(client,mydb,mycursor))
    await client.add_cog(Economy(client,mydb,mycursor))
    await client.add_cog(Loger(client))
    await client.add_cog(Reactor(client))

#@client.command()
#async def hello(ctx):
    #await ctx.send("Currently Functional")
token = os.getenv("BOT_TOKEN")
if token != None:
    client.run(token)
