import discord
from discord.ext import commands
from asyncio import sleep
from configparser import ConfigParser
import datetime

class events:
    """Events"""
    def __init__(self, bot):
        self.bot = bot
        parser = ConfigParser()
        parser.read('./data/config/config.ini')
        self.role_id = parser['channel']['id']

    async def on_voice_state_update(self, before, after):
        if not (after.voice.voice_channel):
            await self.bot.remove_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])
        elif (after.voice.voice_channel):
            await self.bot.add_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])

    async def on_member_remove(self,member):
        time_since_join = int((datetime.datetime.utcnow() - member.joined_at).total_seconds())
        if time_since_join > int(500):
            print(str(time_since_join))
            await self.bot.send_message(member.server, "Thanks for your patronage, %s, please come again." % member.name)


    async def on_member_join(self, member):
        if member.bot:
            return
        channel = self.bot.get_channel("290026887114391552")
        await self.bot.send_message(channel, "Welcome to KUD, %s. You will be given access to talk outside of <#%s> in 5 minutes. **Feel free to communicate with any of the staff members while you're in here.**" % (member.mention, channel.id))
        image_role = [x for x in member.server.roles if x.name == "Media"][0]
        suggestion_role = [x for x in member.server.roles if x.name == "Suggestion"][0]
        role_list = [image_role, suggestion_role]
        await self.bot.add_roles(member, role_list[0], role_list[1])
        await sleep(300)
        await self.bot.add_roles(member, [x for x in member.server.roles if x.name == "Member"][0])

def setup(bot):
    bot.add_cog(events(bot))
