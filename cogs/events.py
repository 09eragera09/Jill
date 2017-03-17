import discord
from discord.ext import commands

class events:
    """Events"""
    def __init__(self, bot):
        self.bot = bot

    async def on_voice_state_update(self, before, after):
        if not (after.voice.voice_channel):
            await self.bot.remove_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])
        elif (after.voice.voice_channel):
            await self.bot.add_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])

    async def on_member_remove(self,member):
        await self.bot.send_message(member.server, "Thanks for your patronage, %s, please come again." % member.name)

    async def on_member_join(self, member):
        channel = self.bot.get_channel("290026887114391552")
        await self.bot.send_message(channel, "Welcome to KUD, %s. You will be given access to talk outside of <#%s> in 5 minutes. **Feel free to communicate with any of the staff members while you're in here.**" % (member.mention, channel.id))

def setup(bot):
    bot.add_cog(events(bot))