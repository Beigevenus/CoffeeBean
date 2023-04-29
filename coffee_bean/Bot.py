import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents(message_content=True, guilds=True)


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="{/}", intents=intents)

    async def setup_hook(self) -> None:
        for extension in os.listdir("./commands"):
            if extension.endswith(".py"):
                await self.load_extension(f"commands.{extension[:-3]}")

        self.tree.copy_global_to(guild=discord.Object(id=os.getenv("GUILD_ID")))
        await self.tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))


bot = Bot()
bot.run(os.getenv("TOKEN"))
