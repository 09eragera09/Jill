import discord
from discord.ext import commands
import logging
import asyncio
import os
from cogs.utils import checks

description = """Jill, a shitty bot written in Python, based off of Chiaki"""
loop = asyncio.get_event_loop()
asyncio.get_child_watcher().attach_loop(loop)
bot = commands.Bot(command_prefix="!", description=description, pm_help=True, loop = loop)

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
    await asyncio.sleep(1)
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