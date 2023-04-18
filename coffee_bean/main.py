import os
import discord
import sqlite3
from typing import Literal, get_args
from dotenv import load_dotenv
from discord import app_commands
from queries import *

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


# General commands
@tree.command(name="poke", description="Poke the bot to see if it's alive!",
              guild=discord.Object(id=os.getenv("GUILD_ID")))
async def poke(interaction):
    await interaction.response.send_message(content="#>~<#", ephemeral=True)


# Intro commands
@tree.command(name="add-intro", description="Saves a link to your intro for others to find easier.",
              guild=discord.Object(id=os.getenv("GUILD_ID")))
async def add_intro(interaction: discord.Interaction, message_id: str):
    result = query_db(SELECT_MEMBER_ID, (interaction.user.id,))

    partial_msg = client.get_partial_messageable(interaction.channel_id)
    try:
        msg: discord.Message = await partial_msg.fetch_message(int(message_id))
    except discord.errors.NotFound:
        await interaction.response.send_message(content=f"I can't find a message with that ID!", ephemeral=True)
    else:
        if msg.author.id == interaction.user.id:
            # Check if the invoker is the one who sent the intro message before doing anything
            if result:
                query_db(UPDATE_INTRO_LINK, (msg.jump_url, interaction.user.id))
                await interaction.response.send_message(content=f"Okay, I've updated that!", ephemeral=True)
            else:
                query_db(INSERT_INTRO, (interaction.user.id, msg.jump_url))
                await interaction.response.send_message(content=f"Okay, I've added that!", ephemeral=True)
        else:
            await interaction.response.send_message(content=f"That message is not your intro, so I won't add it!",
                                                    ephemeral=True)


@tree.command(name="find-intro", description="Looks up an intro for the specified member.",
              guild=discord.Object(id=os.getenv("GUILD_ID")))
async def find_intro(interaction, member: discord.Member):
    result = query_db(SELECT_INTRO_LINK, (member.id,))

    if result:
        await interaction.response.send_message(content=f"Here you go: {result[0][0]}", ephemeral=True)
    else:
        await interaction.response.send_message(content=f"Sorry, that member doesn't seem to have added an intro!",
                                                ephemeral=True)


# RP commands
@tree.command(name="menu", description="Shows the café's menu.", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def menu(interaction, format: Literal["image", "text"] = "image"):
    if format == "card":
        await interaction.response.send_message(file=discord.File(r"./resources/images/menu.jpg"), ephemeral=True)
    elif format == "text":
        await interaction.response.send_message(content=f"Here's a more *digestible* menu:\n{', '.join(menu_list)}",
                                                ephemeral=True)

# TODO: Implement table threads using Interaction.channel and TextChannel.create_thread()


def query_db(query: str, vars: tuple) -> list:
    conn = sqlite3.connect(os.getenv("DB_PATH"))

    with conn:
        cursor = conn.execute(query, vars)
        result = cursor.fetchall()

    return result


client.run(os.getenv("TOKEN"))
