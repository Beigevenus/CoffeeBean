import os
import discord
from dotenv import load_dotenv
from discord import app_commands
# from score_calculator.ScoreCalculator import ScoreCalculator

load_dotenv()

intents = discord.Intents(message_content=True, guilds=True)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# sc = ScoreCalculator()


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
    print("Ready!")


# @tree.command(name="recommend", description="Provides a recommendation of whether to verify a user or not given a "
#                                             "message ID", guild=discord.Object(id=os.getenv("GUILD_ID")))
# async def recommend(interaction, message_id: str):
#     if is_mod(interaction.user, interaction.guild):
#         partial_msg = client.get_partial_messageable(interaction.channel_id)
#
#         try:
#             msg: discord.Message = await partial_msg.fetch_message(int(message_id))
#             recommendation = sc.evaluate(msg.content)
#             await interaction.response.send_message(content=f"```{recommendation}```", ephemeral=True)
#         except discord.errors.NotFound:
#             await interaction.response.send_message(content=f"```ERROR: I wasn't able to find the message with ID "
#                                                             f"{message_id}.```", ephemeral=True)
#     else:
#         await interaction.response.send_message(content="```You don't have permission to use this command!```",
#                                                 ephemeral=True)


@tree.command(name="verify", description="Verifies a user.", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def verify(interaction, member: discord.Member):
    roles = [
        interaction.guild.get_role(952916636669710367),
        interaction.guild.get_role(952916837958569994),
        interaction.guild.get_role(952917220265181214),
        interaction.guild.get_role(952917088694054932),
        interaction.guild.get_role(982188895372451870),
        interaction.guild.get_role(975397798780473344),
        interaction.guild.get_role(975398729332953129),
        interaction.guild.get_role(939552461553803345),
    ]

    if is_mod(interaction.user, interaction.guild):
        # Assign roles to user
        for role in roles:
            await member.add_roles(role)

        await member.remove_roles(interaction.guild.get_role(939552481791340626))

        await interaction.response.defer()

        # Create transcript of ticket
        await interaction.followup.send(content="$transcript")

        # Delete ticket
        await interaction.followup.send(content="$close")
        await interaction.followup.send(content="$delete")

    else:
        await interaction.response.send_message(content="```You don't have permission to use this command!```",
                                                ephemeral=True)


@tree.command(name="reject", description="Rejects a user.", guild=discord.Object(id=os.getenv("GUILD_ID")))
async def reject(interaction):
    if is_mod(interaction.user, interaction.guild):
        pass
    else:
        await interaction.response.send_message(content="```You don't have permission to use this command!```",
                                                ephemeral=True)


def is_mod(member, guild) -> bool:
    role = guild.get_role(939555760004812801)    # ID for Waiter role
    if role in member.roles:
        return True
    else:
        return False


client.run(os.getenv("TOKEN"))
