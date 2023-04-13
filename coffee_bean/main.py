import os
import discord
from typing import Literal, get_args
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

intents = discord.Intents(message_content=True, guilds=True)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

Menu = Literal["Bi-curious Bagel Bites", "Gender-bender Burger", "Grilled Queer-ini", "Non-binary Nachos",
               "Pogayto Salad", "Sapphic Skewers", "Louis' Twinky Tacos", "Nova's Space Dust", "Zoe's Snail Supremo",
               "Bisexual Brownies", "Rainbow Roll Cake", "Trans-tastic Trifle", "Estrogen Espresso", "Fruity Fizzles",
               "Genderfluid", "HR-Tea", "Pipeline Punch", "Neptunic Nectar", "Testosterone Truffle Mocha"]
menu_list: list[Menu] = list(get_args(Menu))


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print("Ready!")


@tree.command(name="poke", description="Poke the bot to see if it's alive!",
              guild=discord.Object(id=os.getenv("GUILD_ID")))
async def poke(interaction):
    await interaction.response.send_message(content="#>~<#", ephemeral=True)


@tree.command(name="menu", description="Shows the café's menu.", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def menu(interaction, fancy: bool = True):
    if fancy:
        await interaction.response.send_message(file=discord.File(r"./resources/images/menu.jpg"), ephemeral=True)
    else:
        await interaction.response.send_message(content=f"Here's a more *digestible* menu:\n{', '.join(menu_list)}",
                                                ephemeral=True)


client.run(os.getenv("TOKEN"))
