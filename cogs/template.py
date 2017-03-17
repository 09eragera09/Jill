import discord
from discord.ext import commands

class thecog:
    """Default Cog Template"""
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(thecog(bot))