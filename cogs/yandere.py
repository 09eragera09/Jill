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

    @commands.command(name='yandere', aliases=['nsfw', 'sfw'], pass_context=True)
    async def yandere_search(self, ctx, *, tags: str = ""):
        """Aliases !nsfw and !sfw for specific rated images, accepts tags"""
        nsfw = [x for x in ctx.message.server.channels if x.name == "nsfw"][0]
        images = [x for x in ctx.message.server.channels if x.name == "images"][0]
        cmd = ctx.invoked_with
        tags = tags.split()
        tags.append("order:random -partial scan")
        check = None
        if cmd == 'yandere':
            if ctx.message.channel in [nsfw, images]:
                if ctx.message.channel == images:
                    check = "some string"
            else:
                await self.bot.say("Please try again in an image channel such as <#%s> or <#%s>" % (images.id, nsfw.id))
                return
        elif cmd == 'sfw':
            if ctx.message.channel in [nsfw, images]:
                tags.append("rating:s")
            else:
                await self.bot.say("Please try again in an image channel such as <#%s> or <#%s>" % (images.id, nsfw.id))
                return
        elif cmd == 'nsfw':
            if ctx.message.channel == nsfw:
                tags.append("-rating:s")
            else:
                await self.bot.say("Please try again in an nsfw channel such as <#%s>" % nsfw.id)
                return
        tags = ' '.join(tags)
        try:
            try:
                image_list = self.yandere.post_list(limit=20, tags=tags)
            except pybooru_errors.PybooruHTTPError:
                await self.bot.say("You have entered too many tags. Please learn to restrain yourself")
            image = choice(image_list)
            image_url = image['sample_url']
        except IndexError:
            await self.bot.say("Nothing found. Please check the spelling or try again with different tags")
            return
        if image['rating'] != 's':
            title = "NSFW Image"
        else:
            title = "SFW Image"
        if image['rating'] != 's' and check is not None:
            await self.bot.say("This image is too lewd for this channel, please try again with `!sfw` or append a `rating:s` to the tags")
            return
        tags = tags.split(' ')
        tags = '+'.join(tags)
        embed = discord.Embed(title=title, url='https://yande.re/post/show/%s' % image['id'])
        embed.set_author(name="Search Results", url='https://yande.re/post?tags=%s' % tags)
        embed.set_image(url=image_url)
        embed.set_footer(text="Image might take a while to appear | Disclaimer: The user is responsible for his searches. The bartender cares not.")
        await self.bot.say(embed=embed)







def setup(bot):
    bot.add_cog(yandere(bot))

    # @commands.cooldown(5, 10, commands.BucketType.user)