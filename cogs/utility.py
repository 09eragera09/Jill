import discord
from discord.ext import commands
import cogs.utils.role_name_grabber as utils
from time import strftime
from asyncio import sleep
from cogs.utils import checks
from time import perf_counter
from sys import exit

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
        """Userinfo command. Par for the course"""
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
        embed.set_footer(text="Userinfo, a method on the shitty python bot Jill", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.say(embed=embed)

    @commands.command(name='avatar', aliases=['ava', 'avi'], pass_context=True)
    async def avatar(self, ctx, user: str = None):
        """Gets Avatar"""
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
        """Reminder command"""
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

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        "pong!"
        t1 = perf_counter()
        await self.bot.send_typing(ctx.message.channel)
        t2 = perf_counter()
        pingtime = t2 - t1
        pingtime *= 1000
        message = "Here's your drink."
        description = "Time taken: %dms" % pingtime
        text = "Drink ordered by: %s#%s" %(ctx.message.author.name, ctx.message.author.discriminator)
        if checks.is_owner():
            message = message.rstrip('.') + ", Boss!"
        embed = discord.Embed(title=message, description=description)
        embed.set_footer(text=text)
        await self.bot.say(embed=embed)

    @commands.command()
    @checks.is_owner()
    async def shutdown(self):
        """Shuts the bot down"""
        await self.bot.say("Boss, Im taking my break.")
        self.bot.close()
        exit()

def setup(bot):
    bot.add_cog(utility(bot))
