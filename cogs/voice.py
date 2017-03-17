import discord
from discord.ext import commands
import os
from random import shuffle
from cogs.utils import checks

class voice:
    """Plays Valhalla OST for no reason at all"""
    def __init__(self, bot):
        self.bot = bot
        discord.opus.load_opus("libopus.so.0")

    @commands.command(name="tunes", aliases=["me_too,_thanks", "jukebox"])
    @checks.is_owner()
    async def connect_to_voice(self):
        """To have the bot play nice Jukebox music"""
        channel = self.bot.get_channel("279686810894860298")
        self.voice = await self.bot.join_voice_channel(channel)
        music_list = [x for x in os.listdir('./cogs/assets/music') if os.path.isfile(os.path.join('./cogs/assets/music', x))]
        await self.bot.say("Ok, Ill start up the Jukebox.")
        self.play_list(music_list, self.voice)

    @commands.command(name="stop", aliases=["pls_stop", "disconnect"])
    @checks.is_owner()
    async def actually_stop(self):
        """makes the voice client disconnect"""
        await self.voice.disconnect()


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
        music_list_ = [x for x in os.listdir('./cogs/assets/music') if os.path.isfile(os.path.join('./cogs/assets/music', x))]
        if num is None:
            listy = ["Currently we have the following songs in the Jukebox, please pick a song number from the list.\n"]
            for i in range(len(music_list_)):
                listy.append("%d. %s" % (i, music_list_[i].rstrip(".ogg").replace("_", " ").title()))
            await self.bot.say('\n'.join(listy))
        else:
            song = music_list_[int(num)]
            self.music_list.remove(song)
            self.music_list.insert(0, song)
            self.player.stop()

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

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

def setup(bot):
    bot.add_cog(voice(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)