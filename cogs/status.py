import discord
from discord.ext import commands
import cogs.utils.role_name_grabber as utils

class status:
    """Status of the bot, the users, the server among other things"""
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
        embed.set_footer(text="Userinfo, a method on the shitty python bot Chiaki", icon_url=client.user.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(status(bot))