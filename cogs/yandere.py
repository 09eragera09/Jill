from pybooru import Moebooru
import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.get_channel import getChannel
from pybooru import exceptions as pybooru_errors
from random import choice

class yandere:
    """Yandere image search"""

    def __init__(self, bot):
        self.bot = bot
        self.yandere = Moebooru('yandere')

    @commands.command(name='yandere', aliases=['nsfw', 'sfw'])
    async def yandere_search(self, ctx, *, tags: str):
        nsfw = getChannel(ctx.message, 'nsfw')
        images = getChannel(ctx.message, 'images')
        cmd = ctx.invoked_with
        tags = tags + ' order:random'
        if cmd == 'yandere':
            if checks.is_image_chan():
                if checks.is_sfw():
                    tags = tags + ' rating:s'
            else:
                await self.bot.say("Please try again in an image channel such as <#%s> or <#%s>" % (images.id, nsfw.id))
                return
        elif cmd == 'sfw':
            if checks.is_image_chan():
                tags = tags + ' rating:s'
            else:
                await self.bot.say("Please try again in an image channel such as <#%s> or <#%s>" % (images.id, nsfw.id))
                return
        elif cmd == 'nsfw':
            if checks.is_nsfw():
                tags = tags + ' rating:-s'
            else:
                await self.bot.say("Please try again in an nsfw channel such as <#%s>" % nsfw.id)
                return
        try:
            try:
                image_list = self.yandere.post_list(limit=20, tags=tags)
            except pybooru_errors.PybooruHTTPError as e:
                await self.bot.say("You have entered too many tags. Please learn to restrain yourself")
            image = choice(image_list)
            image_url = image['sample_url']
        except IndexError:
            await self.bot.say("Nothing found. Please check the spelling or try again with different tags")
        if image['rating'] != 's':
            title = "NSFW Image"
        else:
            title = "SFW Image"
        tags = tags.split(' ')
        tags = '+'.join(tags)
        embed = discord.Embed(title=title, url='https://yande.re/post/show/%s' % image['id'])
        embed.set_author(name="Search Results", url='https://yande.re/post?tags=%s' % tags)
        embed.set_image(image_url)
        embed.set_footer(text="Image might take a while to appear | Disclaimer: The user is responsible for his searches. The bartender cares not.")
        await self.bot.say(embed)







def setup(bot):
    bot.add_cog(yandere(bot))

    # @commands.cooldown(5, 10, commands.BucketType.user)