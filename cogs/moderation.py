import discord
from discord.ext import commands
from cogs.utils import checks

class moderation:
    """Commands to help with server moderation"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prune', pass_context=True)
    async def _prune(self, ctx, *, content: str = None):
        "Prunes stuff. Can take multiple user names in any order"
        if not ctx.message.author.server_permissions.manage_messages and not(checks.is_owner_check(ctx.message)):
            return

        if content is not None:
            content = content.split()
            num = 0
            for x in content:
                try:
                    num = int(x)
                    break
                except:
                    pass
            to_delete = []
            count = 0
            if ctx.message.mentions:
                for x in ctx.message.mentions:
                    for y in reversed(self.bot.messages):
                        if ctx.message.server == y.server and y.author == x:
                            to_delete.append(y)
                            count += 1
                        if count == num:
                            break
            else:
                for x in reversed(self.bot.messages):
                    if ctx.message.server == x.server:
                        to_delete.append(x)
                        count += 1
                    if count == num:
                        break
            await self.bot.delete_messages(to_delete)

    @commands.command(pass_context=True, aliases = ['ban', 'kick', 'mute', 'unmute'])
    async def moderation(self, ctx):
        """Invoke with the specifc command you want."""
        message = ctx.message
        authorize = False
        if message.channel.is_private:
            return
        if checks.is_owner_check(message):
            authorize = True
        cmd = ctx.invoked_with
        if message.mentions and not message.mention_everyone:
            for member in message.mentions:
                if cmd == "ban" and (authorize or message.author.server_permissions.ban_members):
                    await self.bot.ban(member)
                if cmd == "kick" and (authorize or message.author.server_permissions.kick_members):
                    await self.bot.kick(member)
                if cmd == "mute" and (authorize or message.author.server_permissions.manage_roles):
                    if not "Muted" in [x.name for x in member.server.roles]:
                        await self.bot.create_role(member.server, name="Muted", permissions=discord.Permissions.none())
                        await self.bot.send_message(member.server.owner,
                                                    "The `Muted` role has been added to the server, please give it the required channel permissions")
                    await self.bot.add_roles(member, [x for x in member.server.roles if x.name == "Muted"][0])
                if cmd == "unmute" and (authorize or message.author.server_permissions.manage_roles):
                    if not "Muted" in [x.name for x in member.roles]:
                        await self.bot.say("This user is not Muted, so not unmuted")
                    await self.bot.remove_roles(member, [x for x in member.roles if x.name == "Muted"][0])

    @commands.command(pass_context=True)
    async def banme(self, ctx, *, content: str = None):
        """Ban yourself nigga"""
        if content is not None:
            if content in ['pls', 'please']:
                await self.bot.ban(ctx.message.author)
        else:
            await self.bot.say("No.")


    @commands.command(pass_context=True, hidden=True)
    @checks.mod_or_permissions()
    async def unban(self, ctx):
        """Unbans people, WIP"""
        for member in ctx.message.mentions:
            await self.bot.unban(member)

def setup(bot):
    bot.add_cog(moderation(bot))

    #@commands.cooldown(5, 10, commands.BucketType.user)
