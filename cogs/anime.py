import discord
from discord.ext import commands
from cogs.utils import yama

class anime:
    """Default Cog Template"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(anime(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)