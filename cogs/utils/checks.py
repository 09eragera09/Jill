import discord
from discord.ext import commands
from configparser import ConfigParser
from cogs.utils.get_channel import getChannel

config = ConfigParser()
config.read('data/config/config.ini')

def is_owner_check(message):
    if message.author.id == "94374744576512000":
        return True
    return False

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

def is_owner_or_admin():
    return commands.check(lambda ctx: is_owner_check(ctx.message)) or commands.has_permissions(administrator=True)

def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None

def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Bot Mod', 'Bot Admin', 'Staff'), **perms)

    return commands.check(predicate)

def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Staff'), **perms)

    return commands.check(predicate)

def is_nsfw():
    return commands.check(lambda ctx: is_nsfw_channel_check(ctx.message))

def is_nsfw_channel_check(message):
    if message.channel.id in [getChannel(message, message.channel.name).id]:
        return True
    elif "nsfw" in message.channel.name:
        return True
    return False

def is_sfw():
    return commands.check(lambda ctx: is_sfw_channel_check(ctx.message))

def is_sfw_channel_check(message):
    if message.channel.id in [getChannel(message, message.channel.name)]:
        return True
    elif "sfw" in message.channel.name:
        return True
    elif "images" in message.channel.name:
        return True
    return False

def is_image_chan():
    if is_nsfw() or is_sfw():
        return True
    else:
        return False
