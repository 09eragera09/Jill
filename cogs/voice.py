import discord
from discord.ext import commands
import os
from random import shuffle

class voice:
    """Plays Valhalla OST for no reason at all"""
    def __init__(self, bot):
        self.bot = bot
        discord.opus.load_opus("libopus.so.0")

    @commands.command(name="tunes", aliases=["me_too,_thanks", "jukebox"])
    async def connect_to_voice(self):
        """To have the bot play nice Jukebox music"""
        channel = discord.utils.get(self.bot.get_all_channels(), name="VA-11 HALL-A Bar", type=discord.ChannelType.voice, server__id="234643592528789505")
        self.voice = await self.bot.join_voice_channel(channel)
        music_list = [x for x in os.listdir('./cogs/assets/music') if os.path.isfile(os.path.join('./cogs/assets/music', x))]
        await self.bot.say("Ok, Ill start up the Jukebox.")
        self.play_list(music_list, self.voice)

    def play_list(self, music_list, voice):
        self.position = 0
        shuffle(music_list)
        self.music_list = music_list

        def start_next():
            if self.position < len(music_list):
                path = "./cogs/assets/music/" + music_list[0]
                player = voice.create_ffmpeg_player(path, after=start_next)
                self.song = music_list[0].rstrip(".ogg").replace("_", " ").title()
                player.start()
                self.player = player
                self.position += 1
                music_list.append(music_list.pop(0))
            else:
                self.play_list(music_list, voice)
        start_next()

    @commands.command(name="skip", aliases=["boo"])
    async def skip_song(self):
        """To make the bot skip the current song"""
        await self.bot.say("Skipping %s" % self.song)
        self.player.stop()

    @commands.command(name="play")
    async def play_a_song(self, num: str = None):
        if num is None:
            await self.bot.say()
        else:
            return


    @commands.command(name="stop", aliases=["pls_stop", "disconnect"])
    async def actually_stop(self):
        """makes the client disconnect"""
        await self.voice.disconnect()

    @commands.command(name="list")
    async def song_list(self):
        """Get the current queue of songs, upto 8"""
        listx = []
        listx.append("Current Song is **%s**\n\nCurrently Queued songs are:\n" % self.song)
        num = 0
        for i in range(8):
            song = self.music_list[num].rstrip(".ogg").replace("_", " ").title()
            message = "%d. %s" % (num + 1, song)
            listx.append(message)
            num += 1
        await self.bot.say('\n'.join(listx))

    #@commands.command(name="")

def setup(bot):
    bot.add_cog(voice(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)