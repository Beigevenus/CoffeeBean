from typing import Literal, get_args
import discord
from discord.ext import commands
from discord import app_commands
from coffee_bean.db.db_handler import *
from coffee_bean.db.queries import *

Menu = Literal["Bi-curious Bagel Bites", "Gender-bender Burger", "Grilled Queer-ini", "Non-binary Nachos",
               "Pogayto Salad", "Sapphic Skewers", "Louis' Twinky Tacos", "Nova's Space Dust", "Zoe's Snail Supremo",
               "Bisexual Brownies", "Rainbow Roll Cake", "Trans-tastic Trifle", "Estrogen Espresso", "Fruity Fizzles",
               "Genderfluid", "HR-Tea", "Pipeline Punch", "Neptunic Nectar", "Testosterone Truffle Mocha"]
menu_list: list[Menu] = list(get_args(Menu))


class RPCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="opt-in", description="Opt-in to all the fun RP stuff!")
    async def opt_in(self, interaction):
        pass

    @app_commands.command(name="opt-out",
                          description="Opt-out of all RP stuff! WARNING: This will erase all your RP data!")
    async def opt_out(self, interaction, confirm: bool = False):
        if confirm:
            pass
        else:
            await interaction.response.send_message(
                content=f"WARNING: If you opt out of RP, all of your information will "
                        f"be deleted, including your balance, inventory, etc.\nIf "
                        f"you're sure you wish to do this, please run the `/opt-out` "
                        f"command again with `confirm` set to True.",
                ephemeral=True)

    @app_commands.command(name="menu", description="Shows the café's menu.")
    async def menu(self, interaction, format: Literal["image", "text"] = "image"):
        if self.is_opted_in(interaction.user.id):
            if format == "card":
                await interaction.response.send_message(file=discord.File(r"./resources/images/menu.jpg"),
                                                        ephemeral=True)
            elif format == "text":
                await interaction.response.send_message(
                    content=f"Here's a more *digestible* menu:\n{', '.join(menu_list)}",
                    ephemeral=True)
        else:
            await interaction.response.send_message(content="You need to opt in to RP before being able to use this"
                                                            "command. Please refer to the `/opt-in` command",
                                                    ephemeral=True)

    # TODO: Implement table threads using Interaction.channel and TextChannel.create_thread()

    @staticmethod
    def is_opted_in(member_id: str) -> bool:
        result = query_db(SELECT_MEMBER_ID, (member_id,))

        if result:
            if result[0][0] == 0:
                return False
            elif result[0][0] == 1:
                return True
        else:
            query_db(INSERT_MEMBER, (member_id,))
            return False


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RPCommands(bot))
