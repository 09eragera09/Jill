import discord
from discord.ext import commands
import cogs.utils.role_name_grabber as utils
from time import strftime
from asyncio import sleep
from cogs.utils import checks
from time import perf_counter, time
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
        text = "Drink ordered by: %s#%s" %(ctx.message.author.name, ctx.message.author.discriminator)
        if checks.is_owner_check(ctx.message):
            message = message.rstrip('.') + ", Boss!"
        embed = discord.Embed(title=message, description="Time taken: %dms" % pingtime, color=0x9A32CD)
        embed.set_footer(text=text)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        "Gets serverinfo, what else"
        server = ctx.message.server
        embed = discord.Embed(title=server.name, description="Up and running since %s. That's about %s days!" % (server.created_at.strftime("%d %b %Y %H:%M"), (ctx.message.timestamp - server.created_at).days), color=0x9A32CD)
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Region", value=server.region)
        embed.add_field(name="Users", value="%d Online/%d Total Users" % (len([m for m in server.members if m.status != discord.Status.dnd]), server.member_count))
        embed.add_field(name="Text Channels", value=str(len([x for x in server.channels if x.type == discord.ChannelType.text])))
        embed.add_field(name="Voice Channels", value=str(len([x for x in server.channels if x.type == discord.ChannelType.voice])))
        embed.add_field(name="Roles", value=str(len(server.roles)))
        embed.add_field(name="Owner", value="%s#%s" % (server.owner.name, server.owner.discriminator))
        embed.set_footer(text="Server ID: %s" % (server.id))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def welcomecard(self):
        """For those people who expect me to hand them a working welcome card bot all by itself"""
        await self.bot.say(embed="Interested in using the welcome card that you see on this server? Sadly that is not possible. While the bot in itself is open source and allows you to take a look at its code, I will not be helping you with that process, and aditionally the welcome card image is off-limits. If you do use the welcome image, and I hear of it, I will abuse my power to kick/ban you from this server. Thanks for reading.")

    @commands.command()
    @checks.is_owner()
    async def shutdown(self):
        """Shuts the bot down"""
        await self.bot.say("Boss, Im taking my break.")
        self.bot.close()
        exit()

    def getTime(self):
        return time()

    async def on_ready(self):
        global bot_startup
        bot_startup = self.getTime()
        game = discord.Game
        await self.bot.change_presence(game=game(name="VA-11 HALL-A"))

    @commands.command(hidden=True)
    @checks.is_owner()
    async def setGame(self, *, game_name: str = None):
        game = discord.Game
        await self.bot.change_presence(game=game(name=game_name))

    def calculateTime(self, totalseconds):
        totalminutes = int(totalseconds / 60)
        seconds = int(totalseconds % 60)
        totalhours = int(totalminutes / 60)
        minutes = int(totalminutes % 60)
        totaldays = int(totalhours / 24)
        hours = int(totalhours % 24)

        return [totaldays, hours, minutes, seconds]

    @commands.command()
    async def status(self):
        """Get the bot status"""
        embed = discord.Embed(title="%s#%s" % (self.bot.user.name, self.bot.user.discriminator),
                              description="A bot written in python", color=0x9A32CD)
        embed.add_field(name="Owner", value="Era#4669", inline=False)
        currentTime = self.getTime()
        seconds = int(currentTime - bot_startup)
        uptime = self.calculateTime(seconds)
        embed.add_field(name="Uptime",
                        value="Have been mixing drinks for %sd%sh%sm%ss" % (uptime[0], uptime[1], uptime[2], uptime[3]),
                        inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(utility(bot))
