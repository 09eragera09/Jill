import discord
from discord.ext import commands
from random import choice

class fun:
    """Commands that do not affect the functionality of the bot, only for users"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def _test(self):
        """test command"""
        await self.bot.say("This is a test message")

    @commands.command()
    async def textface(self, face: str):
        """replies with text faces, use !textfaces <textface>"""
        textface_dict = {'lenny': '( ͡° ͜ʖ ͡°)', 'shrug': '¯\_(ツ)_/¯', 'fiteme': '(ง ͠° ͟ل͜ ͡°)ง', 'flip': '(╯°□°）╯︵ ┻━┻', 'unflip': '┬──┬ ノ( ゜-゜ノ)', 'hug': '༼ つ ◕_◕ ༽つ'}
        emoji = textface_dict[face]
        await self.bot.say(emoji)

    @commands.command(name='8ball')
    async def _8ball(self):
        """ask the magic 8ball for answers to your yes or no questions"""
        magicball = ['It is certain', 'It is decidedly so', 'Without a doubt',
                     'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Most likely',
                     'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now',
                     'Concentrate and ask again', 'Don\'t count on it', 'My reply is no',
                     'My sources say no', 'Outlook not so good', 'Very doubtful']
        await self.bot.say(choice(magicball))

    @commands.command()
    async def shitwaifu(self):
        '''your waifu is shit'''
        await self.bot.say("http://azelf.net/mfw/shitwaifu.png")

    @commands.command()
    async def urban(self, *, search: str):
        '''urban dictionary best dictionary'''
        search = search.split()
        search = '+'.join(search)
        if not(search):
            await self.bot.say("Please enter an argument")
        else:
            await self.bot.say('http://www.urbandictionary.com/define.php?term=%s' % search)

    @commands.command(name='mal', aliases=["kitsu, anilist"], pass_context=True)
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
    async def enlarge(self, emote : str):
        emote_id = emote.split(":")[-1].rstrip('>')
        await self.bot.say("Custom emote has been enlarged, https://discordapp.com/api/emojis/%s.png" % emote_id)


#    @commands.command()
 #   async def bartender(self, *, flavor: str):
  #      drinks = {}

def setup(bot):
    bot.add_cog(fun(bot))
