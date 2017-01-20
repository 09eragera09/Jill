import discord
from discord.ext import commands
import cogs.utils.role_name_grabber as utils
from time import strftime
from asyncio import sleep
from cogs.utils import checks
from time import time

class utility:
    """Utility"""
    def __init__(self, bot):
        self.bot = bot

    async def gameCheck(self, member):
        if not (member.game):
            return "Not playing anything"
        else:
            return str(member.game.name)

    @commands.command(name='userinfo', pass_context=True)
    async def userinfo(self, ctx, *, username: str = None):
        if username is None:
            username = ctx.message.author.name
        elif ctx.message.mentions and not ctx.message.mention_everyone:
            username = ctx.message.mentions[0].name
        member = ctx.message.server.get_member_named(username)
        role_list = await utils.role_name_grabber(member)
        role_list_joined = ", ".join(role_list[1:])
        game = await self.gameCheck(member)
        embed = discord.Embed(title="❯ Member Details", description="• Nickname: %s\n• Roles: %s\n• Joined at: %s" % (member.nick, role_list_joined, member.joined_at.strftime("%A, %B %d, %Y, %I:%M %p")), color=0x9A32CD)
        embed.add_field(name="❯ User Details", value="• Created at: %s\n• Status: %s\n• Game: %s" % (member.created_at.strftime("%A, %B %d, %Y, %I:%M %p"), member.status, game), inline=True)
        embed.set_author(name="%s#%s" % (member.name, member.discriminator), icon_url=member.avatar_url)
        embed.set_footer(text="Userinfo, a method on the shitty python bot Chiaki", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.say(embed=embed)

    @commands.command(name='avatar', aliases=['ava', 'avi'], pass_context=True)
    async def avatar(self, ctx, user: str = None):
        if user is None:
            user = ctx.message.author
        elif ctx.message.mentions and not ctx.message.mention_everyone:
            user = ctx.message.mentions[0]
        else:
            user = ctx.message.server.get_member_named(user)
        embed = discord.Embed()
        embed.set_image(url=user.avatar_url)
        embed.set_author(name="%s#%s" % (user.name, user.discriminator), icon_url=user.avatar_url)
        await self.bot.say(embed=embed)

    @commands.command(name='remind', aliases=['remindme', 'reminder'], pass_context=True)
    async def _remind(self, ctx, timestr: str, format: str, *, msg: str):
        try_again = "Please try again. It should be in the form of `!remind (a number) (hours/minutes/seconds) (a message)`"
        try:
            time = int(timestr)
        except:
            await self.bot.say(try_again)
        date = strftime("%Y-%m-%d %H:%M")
        if format in ["second", "seconds"]:
            await self.bot.say("You will be sent a reminder through DM in %s second(s)!" % timestr)
            await sleep(time)
        elif format in ["minutes", "minute"]:
            time *= 60
            await self.bot.say("You will be sent a reminder through DM in %s minute(s)!" % timestr)
            await sleep(time)
        elif format in ["hours", "hour"]:
            time = time * 60 * 60
            await self.bot.say("You will be sent a reminder through DM in %s hour(s)" % timestr)
            await sleep(time)
        else:
            await self.bot.say(try_again)
            return
        await self.bot.whisper("You had set a reminder on %s GMT for the following message: %s" % (date, msg))

    @commands.command()
    async def ping(self):
        if checks.is_owner():
            message = "Your net is working, Era-kun!"
        else:
            message = "Pong!"
        ping = self.bot.say(message)
        tmptime = time()
        await self.bot.get_message(message.channel, ping.id)
        tmptime1 = time()
        pingtime = tmptime1 - tmptime
        pingtime *= 1000
        message += "`%dms`" %pingtime


    @commands.command()
    @checks.is_owner()
    async def sleep(self):
        await self.bot.say("Boss, Im taking my break.")
        self.bot.close()
        sys.exit()

def setup(bot):
    bot.add_cog(utility(bot))
