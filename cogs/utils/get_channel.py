import discord

async def getChannel(message, channel_name):
    channel = [x for x in message.server.channels if x.name == channel_name][0]
    return channel
