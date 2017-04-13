import discord, math
from discord.ext import commands
from cogs.utils import checks

class general:
    """General stuff"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def urban(self, *, search: str):
        '''urban dictionary best dictionary'''
        search = search.split()
        search = '+'.join(search)
        if not(search):
            await self.bot.say("Please enter an argument")
        else:
            await self.bot.say('http://www.urbandictionary.com/define.php?term=%s' % search)

    @commands.command(name='mal', aliases=["kitsu", "anilist"], pass_context=True)
    async def anime(self, ctx, content: str = None):
        '''gets your animelist, supply with username'''
        cmd = ctx.invoked_with
        if content is not None:
            if cmd == 'mal':
                await self.bot.say('Here\'s your Myanimelist, http://myanimelist.net/animelist/%s' % content)
            if cmd == 'kitsu':
                await self.bot.say('Here\'s your Kitsu library, https://kitsu.io/users/%s/library' % content)
            if cmd == 'anilist':
                await self.bot.say('Here\'s your anilist animelist, https://anilist.co/user/%s/animelist' % content)
        else:
            await self.bot.say("Please enter a username")

    @commands.command()
    async def enlarge(self, emote: str):
        """Enlarges any custom emotes such as ones from NGNL"""
        emote_id = emote.split(":")[-1].rstrip('>')
        await self.bot.say("Custom emote has been enlarged, https://discordapp.com/api/emojis/%s.png" % emote_id)

    @commands.command()
    @checks.is_owner()
    async def say(self, *, msg: str):
        """Makes the bot say stuff. Owner only"""
        await self.bot.say(msg)

    @commands.command()
    async def eval(self, *, var: str):
        """Evaluates stuff."""
        bl = ['**', '__', 'lambda']
        for item in bl:
            if item in var:
                self.bot.say("That is too unsafe for this. Please kill yourself to prevent further damage to owner's system")
                return
        await self.bot.say(eval(var, {'__builtins__': {'math': math, 'sum': sum, 'str': str, 'int': int, 'float': float}}))

    @commands.command()
    async def invite(self):
        '''Invite link to add to more servers'''
        await self.bot.say(
            "Here's my invite link https://discordapp.com/oauth2/authorize?permissions=8&scope=bot&client_id=271241978556055552")

    @commands.command()
    async def source(self):
        '''Get source on github'''
        await self.bot.say("Here's my source code https://github.com/09eragera09/Jill")

    @commands.command(name="clean", aliases=["cleanup", "fuckoffJill"])
    async def clean(self):
        """Cleans up the message channel"""
        to_delete=[]
        for message in reversed(self.bot.messages):
            if message.author == self.bot.user:
                to_delete.append(message)
        await self.bot.delete_messages(to_delete)

    @commands.command(name="role", pass_context=True)
    async def users_that_have_a_particular_role(self, ctx, *, var: str = None):
        """To check how many users have a particular role"""
        if var is None:
            return
        try:
            role = [x for x in ctx.message.server.roles if x.name == var][0]
        except:
            await self.bot.say("No such role exists on server")
            return

        member_list = []

        for member in ctx.message.server.members:
            if role in member.roles:
                member_list.append(member.name)
        await self.bot.say("Currently, the role %s has %d users. The following users have that role: %s" % (var, len(member_list), ', '.join(member_list)))

def setup(bot):
    bot.add_cog(general(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)