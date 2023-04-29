import discord
from discord.ext import commands
from discord import app_commands
from coffee_bean.db.db_handler import *
from coffee_bean.db.queries import *


class IntroCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="add-intro", description="Saves a link to your intro for others to find easier.")
    async def add_intro(self, interaction: discord.Interaction, message_id: str):
        result = query_db(SELECT_MEMBER_ID, (interaction.user.id,))

        partial_msg = self.bot.get_partial_messageable(interaction.channel_id)
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

    @app_commands.command(name="find-intro", description="Looks up an intro for the specified member.")
    async def find_intro(self, interaction, member: discord.Member):
        result = query_db(SELECT_INTRO_LINK, (member.id,))

        if result:
            await interaction.response.send_message(content=f"Here you go: {result[0][0]}", ephemeral=True)
        else:
            await interaction.response.send_message(content=f"Sorry, that member doesn't seem to have added an intro!",
                                                    ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(IntroCommands(bot))
