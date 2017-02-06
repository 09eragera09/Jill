import discord
from discord.ext import commands

class bartender:
    """Default Cog Template"""
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(bartender(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)