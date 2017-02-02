import discord
from discord.ext import commands
from time import time
import logging
from asyncio import sleep, coroutine
from wand.drawing import Drawing, TEXT_ALIGN_TYPES
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
        draw.font_size = 55
        draw.text_alignment = 'right'
        draw.text(x=1465, y=512, body="User: %s#%s" % (member.name, member.discriminator))
        with Image(filename='./cogs/assets/Stella_KUD.png') as image:
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

@bot.group(hidden=True)
@checks.is_owner()
async def cogs():
    pass

@cogs.command(name='reload', hidden=True, pass_context=True)
async def _reload(ctx, *, cogs: str = None):
    await bot.say('Reloading Cogs...', delete_after=10)
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
    embed = discord.Embed(title="Cogs have been reloaded!", color=0x9A32CD)
    embed.set_author(name="Bossu!", icon_url=bot.user.avatar_url)
    if len(load_cogs) != 0:
        msg_loaded = ", ".join(load_cogs).title()
        embed.add_field(name="❯ Cogs that were reloaded:", value=msg_loaded)
    if len(not_loaded) != 0:
        msg_not_loaded = ", ".join(not_loaded).title()
        embed.add_field(name="❯ Cogs that couldn't be reloaded:", value=msg_not_loaded)
    await bot.say(embed=embed)

@cogs.command(name='list')
async def _list():
    all_cogs = [f for f in os.listdir("./cogs") if os.path.isfile(os.path.join("./cogs", f))]
    loaded = []
    unloaded = []
    for cog in all_cogs:
        cog = cog.split(".")[0]
        ccog = bot.get_cog(cog.lower())
        if ccog:
            loaded.append(cog.replace("_", " ").title())
        else:
            unloaded.append(cog.replace("_", " ").title())
    embed = discord.Embed(title="Cogs currently loaded", description="Total Cogs: %d | Loaded : %d | Unloaded : %d" %(len(all_cogs), len(loaded), len(unloaded)), color=0x9A32CD)
    if len(loaded) != 0:
        embed.add_field(name="Loaded Cogs:", value=", ".join(loaded))
    if len(unloaded) != 0:
        embed.add_field(name="Unloaded Cogs:", value=", ".join(unloaded), inline=False)
    await bot.say(embed=embed)


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
    game = discord.Game
    await bot.change_presence(game=game(name="VA-11 HALL-A"))

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
    imageGen(member)
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
    '''Get source on github'''
    await bot.say("Here's my source code https://github.com/09eragera09/Jill")


@bot.command()
async def invite():
    '''Invite link to add to more servers'''
    await bot.say("Here's my invite link https://discordapp.com/oauth2/authorize?&client_id=271241978556055552&scope=bot")


@bot.command(hidden=True)
@checks.is_owner()
async def setGame(*, game_name: str = None):
    game = discord.Game
    await bot.change_presence(game=game(name=game_name))

@bot.command()
async def status():
    """Get the bot status"""
    embed = discord.Embed(title="%s#%s" % (bot.user.name, bot.user.discriminator), description="A bot written in python", color=0x9A32CD)
    embed.add_field(name="Owner", value="Era#4669", inline=False)
    currentTime = getTime()
    seconds = int(currentTime - bot_startup)
    uptime = calculateTime(seconds)
    embed.add_field(name="Uptime", value="Have been mixing drinks for %sd%sh%sm%ss" % (uptime[0], uptime[1], uptime[2], uptime[3]), inline=False)
    embed.set_thumbnail(url=bot.user.avatar_url)
    await bot.say(embed=embed)

@bot.command(name='welcome', aliases=['wleocme'], pass_context=True, hidden=True)
async def wleocme(ctx):
    member = ctx.message.author
    imageGen(member)
    await bot.send_file(member.server, './cogs/assets/test.png', content="Welcome to Kindly United Dreams, %s, Please read the rules over at <#%s>" %(member.mention, [x.id for x in member.server.channels if x.name == "readme"][0]))

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
