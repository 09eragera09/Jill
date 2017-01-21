import discord
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
    async def anime(self, ctx, content: str):
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
    @checks.is_owner()
    async def eval(self, *, var: str):
        """Evaluates stuff. Owner only"""
        await self.bot.say(eval(var))



def setup(bot):
    bot.add_cog(general(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)