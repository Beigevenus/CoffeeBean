import discord
from discord.ext import commands
from discord import app_commands


class UtilityCommands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="add-intro", description="Saves a link to your intro for others to find easier.")
    async def add_intro(self, interaction: discord.Interaction, message_id: str):
        self.bot.ensure_member(interaction.user.id)

        partial_msg = self.bot.get_partial_messageable(interaction.channel_id)
        try:
            msg: discord.Message = await partial_msg.fetch_message(int(message_id))
        except discord.errors.NotFound:
            await interaction.response.send_message(content=f"I can't find a message with that ID!", ephemeral=True)
        else:
            if msg.author.id == interaction.user.id:
                # Check if the invoker is the one who sent the intro message before doing anything
                self.bot.query_db(self.bot.UPDATE_INTRO_LINK, (msg.jump_url, interaction.user.id))
                await interaction.response.send_message(content=f"Okay, I've updated that!", ephemeral=True)
            else:
                await interaction.response.send_message(content=f"That message is not your intro, so I won't add it!",
                                                        ephemeral=True)

    @app_commands.command(name="find-intro", description="Looks up an intro for the specified member.")
    async def find_intro(self, interaction, member: discord.Member):
        result = self.bot.query_db(self.bot.SELECT_INTRO_LINK, (member.id,))

        if result:
            await interaction.response.send_message(content=f"Here you go: {result[0][0]}", ephemeral=True)
        else:
            await interaction.response.send_message(content=f"Sorry, that member doesn't seem to have added an intro!",
                                                    ephemeral=True)

    @app_commands.command(name="add-pronouns",
                          description="Saves your current preferred pronouns for others to find easier.")
    async def add_pronouns(self, interaction, pronouns: str):
        self.bot.ensure_member(interaction.user.id)

        self.bot.query_db(self.bot.UPDATE_PRONOUNS, (pronouns, interaction.user.id))
        await interaction.response.send_message(content=f"Okay, I've updated that!", ephemeral=True)

    @app_commands.command(name="find-pronouns",
                          description="Looks up a member's current preferred pronouns.")
    async def find_pronouns(self, interaction, member: discord.Member):
        result = self.bot.query_db(self.bot.SELECT_PRONOUNS, (member.id,))

        if result and result[0][0] != "None":
            await interaction.response.send_message(content=f"These are the member's current pronouns: {result[0][0]}",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(content=f"Sorry, that member doesn't seem to have set any preferred"
                                                            f" pronouns!",
                                                    ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UtilityCommands(bot))
