import os
import discord
from typing import Literal
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

intents = discord.Intents(message_content=True, guilds=True)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

Order = Literal["stuff", "things"]


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print("Ready!")


@tree.command(name="test", description="Test command", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def test(interaction, order: Order):
    pass


client.run(os.getenv("TOKEN"))
