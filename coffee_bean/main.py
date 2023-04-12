import os
import discord
from typing import Literal, get_args
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

intents = discord.Intents(message_content=True, guilds=True)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

Menu = Literal["stuff", "things"]
menu_list: list[Menu] = list(get_args(Menu))


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print("Ready!")


@tree.command(name="poke", description="Poke the bot to see if it's alive!",
              guild=discord.Object(id=os.getenv("GUILD_ID")))
async def ping(interaction):
    await interaction.response.send_message(content="#>~<#", ephemeral=True)


@tree.command(name="test", description="Test command", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def test(interaction, order: Menu):
    pass


client.run(os.getenv("TOKEN"))
