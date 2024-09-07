import os
import discord
from typing import Final
from dotenv import load_dotenv
from config.logging import logger as log
from config.db import AtlasConfig

load_dotenv(dotenv_path=".env")
STANLIB_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


class Stanlib(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')


if __name__ == "__main__":
    log.info("Starting Stanlib application - @author Hi-kue")
    log.info("Connecting to Atlas MongoDB")
    db = AtlasConfig().mongo_connect()
    log.info(type(db))


