from discord.ext.commands import Bot, when_mentioned_or
from discord import Intents


class WordleBot(Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=when_mentioned_or("w!"), intents=intents, help_command=None)
