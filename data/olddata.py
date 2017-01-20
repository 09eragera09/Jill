@bot.command(pass_context=True)
async def help(ctx):
    """Help message"""
    userhelp = ["There are a few commands you can use.",
                "• `!ping` to check if your net is working ;)",
                "• `!uptime` to check how long the bot has been up",
                "• `!userinfo` to check your or someone else's basic account info",
                "• `!avatar` to get someone's avatar",
                "• `!status` Prints the bot's status",
                "• `!remind` will let you set a reminder.",
                "• `!booru` searches Danbooru, accepts tags, use an underscore, for example, `!booru competition_swimsuit`",
                "• `!sfw` same as above, but with safe images forced",
                "• `!nsfw` same as above, but with explicit images forced",
                "• `!enlarge` enlarges custom emojis such as ones from NGNL",
                "• `!invite` lets you get the bot invite link",
                "• `!8ball` the magic 8ball will reply with either an affirmative, negative or a non-commital response",
                "• `!urban` to check urbandictionary for the definition of a term",
                "• `!mal`, `!hb`, `!anilist` to get your animelist from myanimelist, hummingbird and anilist, respectively.",
                "• `!welcome` to test the welcome card",
                "• `!lenny`, `!fiteme`, `!flip`, `!unflip`, `!hug`, and `!shrug` reply with their respective emojis ",
                "Here's my source code: https://github.com/09eragera09/Jill/blob/master/Jill.py",
                "To invite me to your server, click this link: https://discordapp.com/oauth2/authorize?&client_id=241587632948248586&scope=bot"]

    modhelp = ["• `!prune`, `!ban`, `!kick`, `!mute`, and `!unmute`, do exactly what they say."]

    ownerhelp = ["Commands for Era-kun only",
                 "• `!sleep` makes the bot go offline",
                 "• `!restart` makes the bot restart",
                 "• `!subprocess` makes the bot execute commands in shell"]
    userhelp = '\n'.join(userhelp)
    embed = discord.Embed(title="❯ User Commands", description=userhelp, color=0x9A32CD)
    embed.set_author(name="Command List", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="Jill is a shitty bot written in python", icon_url=bot.user.avatar_url)
    if ctx.message.author.id == "94374744576512000":
        modhelp = '\n'.join(modhelp)
        embed.add_field(name="❯ Mod Commands", value=modhelp)
        ownerhelp = '\n'.join(ownerhelp)
        embed.add_field(name="❯ Owner Commands", value=ownerhelp)
        await bot.whisper(embed=embed)
    elif [x for x in ctx.message.server.roles if x.name == "Staff"][0] in ctx.message.author.roles:
        modhelp = '\n'.join(modhelp)
        embed.add_field(name="❯ Mod Commands", value=modhelp)
        await bot.whisper(embed=embed)
    else:
        await bot.whisper(embed=embed)
