import discord
from discord.ext import commands
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

class welcome:
    """Welcome Card"""
    def __init__(self, bot):
        self.bot = bot

    def imageGen(self, member):
        with Drawing() as draw:
            draw.fill_color = Color('white')
            draw.font = './cogs/assets/Whitney_Medium.ttf'
            draw.font_size = 55
            draw.text_alignment = 'right'
            member_name = member.name.encode()
            member_name = member_name.decode(encoding='ascii', errors='ignore')
            draw.text(x=1465, y=512, body="User: %s#%s" % (member_name, member.discriminator))
            with Image(filename='./cogs/assets/Stella_KUD.png') as image:
                draw(image)
                image.save(filename='./cogs/assets/test.png')
                return None

    async def on_member_join(self, member):
        if member.bot:
            bot_role = [x for x in member.server.roles if x.name == "Lesser Bots"]
            if member.name not in [x.name for x in member.server.roles]:
                await self.bot.create_role(member.server, name=member.name, permissions=discord.Permissions.none())
            await self.bot.add_roles(member, [x for x in member.server.roles if x.name == member.name][0], bot_role)
            return
        self.imageGen(member)
        await self.bot.send_file(member.server, './cogs/assets/test.png',
                            content="Welcome to Kindly United Dreams, %s, Please read the rules over at <#%s>" % (
                            member.mention, [x.id for x in member.server.channels if x.name == "readme"][0]))

    @commands.command(name='welcome', aliases=['wleocme'], pass_context=True, hidden=True)
    async def wleocme(self, ctx):
        member = ctx.message.author
        self.imageGen(member)
        await self.bot.send_file(member.server, './cogs/assets/test.png',
                            content="Welcome to Kindly United Dreams, %s, Please read the rules over at <#%s>" % (
                            member.mention, [x.id for x in member.server.channels if x.name == "readme"][0]))


def setup(bot):
    bot.add_cog(welcome(bot))
