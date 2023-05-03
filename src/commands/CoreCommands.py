from discord.ext import commands
from discord import app_commands


class CoreCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="poke", description="Poke the bot to see if it's alive!")
    async def poke(self, interaction):
        await interaction.response.send_message(content="#>~<#", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoreCommands(bot))
