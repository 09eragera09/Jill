import discord
from discord.ext import commands
from asyncio import coroutine
from pushbullet import PushBullet

class push_bullet:
    """Push Bullet, to send and recieve alerts"""
    def __init__(self, bot):
        self.bot = bot
        pb = PushBullet(api_key=open('pb_token', 'r').read().rstrip("\n"))
        self.phone = pb.get_device('Phone')

    @coroutine
    async def on_message(self, message):
        if message.mentions:
            for x in message.mentions:
                if x.id == "94374744576512000":
                    self.phone.push_note("Hey! Someone mentioned you.", "%s on %s" % (message.author.name, message.server.name))
def setup(bot):
    bot.add_cog(push_bullet(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)