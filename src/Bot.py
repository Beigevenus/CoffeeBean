import os
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents(message_content=True, guilds=True)


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="{/}", intents=intents)
        self.conn = sqlite3.connect(os.getenv("DB_PATH"))
        self.SELECT_MEMBER_ID = "SELECT member_id FROM member WHERE member_id = ?;"
        self.SELECT_INTRO_LINK = "SELECT intro_link FROM member WHERE member_id = ?;"
        self.UPDATE_INTRO_LINK = "UPDATE member SET intro_link = ? WHERE member_id = ?"
        self.INSERT_MEMBER = "INSERT INTO member (member_id) VALUES (?);"
        self.UPDATE_PRONOUNS = "UPDATE member SET pronouns = ? WHERE member_id = ?;"
        self.SELECT_PRONOUNS = "SELECT pronouns FROM member WHERE member_id = ?;"

    async def setup_hook(self) -> None:
        for extension in os.listdir("./commands"):
            if extension.endswith(".py"):
                await self.load_extension(f"commands.{extension[:-3]}")

        self.tree.copy_global_to(guild=discord.Object(id=os.getenv("GUILD_ID")))
        await self.tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))
        print("Ready!")

    def query_db(self, query: str, vars: tuple) -> list:
        with self.conn:
            cursor = self.conn.execute(query, vars)
            result = cursor.fetchall()

        return result

    def ensure_member(self, member_id):
        result = self.query_db(self.SELECT_MEMBER_ID, (member_id,))

        if not result:
            self.query_db(self.INSERT_MEMBER, (member_id,))


bot = Bot()
bot.run(os.getenv("TOKEN"))
