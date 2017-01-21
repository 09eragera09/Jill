import discord
from discord.ext import commands
from time import time
import logging
from asyncio import sleep, coroutine
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color
import traceback
import os
from cogs.utils import checks

description = """Jill, a shitty bot written in Python, based off of Chiaki"""
bot = commands.Bot(command_prefix="!", description=description, pm_help=True)

def imageGen(member):
    with Drawing() as draw:
        draw.fill_color = Color('white')
        draw.font = './cogs/assets/Whitney_Medium.ttf'
        if 15 < len(member.name) < 22:
            draw.font_size = 35
        elif len(member.name) >= 22:
            draw.font_size = 30
        else:
            draw.font_size = 40
        draw.text(x=510, y=350, body="User: %s#%s" % (member.name, member.discriminator))
        with Image(filename='./cogs/assets/KUD_3.png') as image:
            draw(image)
            image.save(filename='./cogs/assets/test.png')
            return None

def getTime():
    return time()

def calculateTime(totalseconds):
    totalminutes = int(totalseconds/60)
    seconds = int(totalseconds % 60)
    totalhours = int(totalminutes / 60)
    minutes = int(totalminutes % 60)
    totaldays = int(totalhours / 24)
    hours = int(totalhours % 24)

    return [totaldays, hours, minutes, seconds]

@bot.command(name='reload', hidden=True, pass_context=True)
@checks.is_owner()
async def _reload(ctx, *, cogs: str = None):
    msg1 = await bot.say('Reloading Cogs...', delete_after=10)
    if cogs is not None:
        cogs = cogs.split(' ')
    elif cogs is None:
        cogs = [x for x in os.listdir('./cogs') if os.path.isfile(os.path.join('./cogs', x))]
    for cog in cogs:
        try:
            bot.get_cog(cog)
        except:
            await bot.say('`'+cog+'` is not a cog.')
    temp = [cog for cog in cogs]
    for cog in cogs:
        bot.unload_extension('cogs.'+cog.replace('.py', ''))
    await sleep(1)
    load_cogs = []
    not_loaded = []
    for cog in cogs:
        try:
            bot.load_extension('cogs.'+cog.replace('.py', ''))
        except Exception:
            not_loaded.append(cog.replace('py', ''))
            raise
        else:
            load_cogs.append(cog.replace('py', ''))
    del temp
    if len(load_cogs) != 0:
        msg_loaded = '***Cogs Reloaded:*** `{}`'.format(", ".join(load_cogs))
        temp.append(msg_loaded)
    if len(not_loaded) != 0:
        msg_not_loaded = '***Cogs Not Loaded:*** `{}`'.format(", ".join(not_loaded))
        temp.append(msg_not_loaded)
    await bot.say(" | ".join(temp).upper(), delete_after=5)
    await sleep(2)
    try:
        await bot.delete_message(ctx.message)
    except:
        pass
    await sleep(5)

@bot.event
async def on_ready():
    print("Logged in as Alice_Rabbit")
    print("Time to mix drinks and change lives!")
    print(bot.user.id)
    print('-' * 20)
    cogs = [x for x in os.listdir('./cogs') if os.path.isfile(os.path.join('./cogs', x))]
    for cog in cogs:
        x = 'cogs.' + cog.replace('.py', '')
        bot.load_extension(x)
    global bot_startup
    bot_startup = getTime()

@coroutine
@bot.event
async def on_message(message):
    try:
        await bot.process_commands(message)
    except discord.ext.commands.errors.DisabledCommand as e:
        await bot.say("*`{}` is disabled*".format(str(e).split(" ")[0]))
    except discord.ext.commands.errors.CheckFailure as e:
        await bot.say("```You do not have permission for this command!```")
    except discord.ext.commands.errors.CommandOnCooldown as e:
        await bot.say("```{}```".format(str(e)))
    except discord.ext.commands.errors.BadArgument as e:
        await bot.say("```{}```".format(str(e)))
    except discord.ext.commands.errors.CommandError as e:
        message.command.dispatch_error(e, message)
        error = traceback.format_exc().split("The above exception was the direct cause of the following exception:")[0]
        await bot.say("An Error Has Occurred: ```py\n{}```".format(error))
    except:
        raise

@bot.event
async def on_voice_state_update(before, after):
    if not(after.voice.voice_channel):
        await bot.remove_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])
    elif (after.voice.voice_channel):
        await bot.add_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])


@bot.event
async def on_member_join(member):
    imagegen = imageGen(member)
    await bot.send_file(member.server, './cogs/assets/test.png', content="Welcome to Kindly United Dreams, %s, Please read the rules over at <#%s>" % (member.mention, [x.id for x in member.server.channels if x.name == "readme"][0]))
    music_role = [x for x in member.server.roles if x.name == "Music"][0]
    image_role = [x for x in member.server.roles if x.name == "Image"][0]
    suggestion_role = [x for x in member.server.roles if x.name == "Suggestion"][0]
    role_list = [music_role, image_role, suggestion_role]
    await bot.add_roles(member, role_list[0], role_list[1], role_list[2])
    await sleep(300)
    await bot.add_roles(member, [x for x in member.server.roles if x.name == "People"][0])


@bot.command()
async def source():
    await bot.say("Here's my source code https://github.com/09eragera09/Jill/blob/master/Jill.py")


@bot.command()
async def invite():
    await bot.say("Here's my invite link https://discordapp.com/oauth2/authorize?&client_id=271241978556055552&scope=bot")


@bot.command()
async def setGame(*, game_name: str = None):
    game = discord.Game
    await bot.change_presence(game=game(name=game_name))

@bot.command()
async def status():
    embed = discord.Embed(title="%s#%s" % (bot.user.name, bot.user.discriminator), description="A bot written in python", color=0x9A32CD)
    embed.add_field(name="Owner", value="Era#4669", inline=False)
    currentTime = getTime()
    seconds = int(currentTime - bot_startup)
    uptime = calculateTime(seconds)
    embed.add_field(name="Uptime", value="have been mixing drinks for %sd%sh%sm%ss" % (uptime[0], uptime[1], uptime[2], uptime[3]), inline=False)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await bot.say(embed=embed)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

global bot_startup
token = open('token', 'r').read()
token = token.rstrip('\n')
while True:
    try:
        bot.run(token)
    except ConnectionResetError:
        pass
    except KeyboardInterrupt:
        break
