import discord
from discord.ext import commands
import datetime
import typing


class Moderation:
    """Cogs made for moderation.
    Include various other stuff as well.
    """

    def __init__(self, bot):
        self.bot = bot
        self.toscd = bot.get_guild(288455332173316106)

    @commands.command()
    async def getuserid(self, ctx, user: discord.User):
        """Get a user's ID. If the bot cannot find the person, try making sure capitalization is followed
        or use the full ping including the discriminator.
        """

        await ctx.send(f'{ctx.author.mention} **||** That user\'s ID is **`{user.id}`**')

    @commands.command()
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def addrole(self, ctx, role: commands.Greedy[discord.Role], user: discord.Member, *, reason='None'):
        """Adds a role to a user.

        Params:
        role - Role(s) to add to the user
        user - A member of the discord
        reason - {optional} for the addition
        You can pass more than one role in at the same time, make sure it is between member and /addrole.
        """

        toscd = self.bot.get_guild(288455332173316106)
        await user.add_roles(*role)
        em = discord.Embed(colour=discord.Colour.green(), description='Logging Entry - `/addrole`')
        em.add_field(name=f'Member:', value=f'{user.mention}')
        em.add_field(name='Role(s) added:', value=', '.join((x.name for x in role)))
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        channel = toscd.get_channel(288467626890362880)
        await channel.send(embed=em)
        await ctx.send(embed=em)
        await user.send('A recipt of a moderator action has been sent to you:', embed=em)

    @commands.command()
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def removerole(self, ctx, role: commands.Greedy[discord.Role], user: discord.Member, *, reason='None'):
        """Removes a role from a user.

        Params:
        role - Role(s) to remove to the user
        user - A member of the discord
        reason - {optional} for the removal
        You can pass more than one role in at the same time, make sure it is between member and /removerole.
        """

        await user.remove_roles(*role)
        em = discord.Embed(colour=discord.Colour.red(), description='Logging Entry - `/removerole`')
        em.add_field(name=f'Member:', value=f'{user.mention}', inline=True)
        em.add_field(name='Role(s) removed:', value=', '.join((x.name for x in role)), inline=True)
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        toscd = self.bot.get_guild(288455332173316106)
        channel = toscd.get_channel(288467626890362880)

        await channel.send(embed=em)
        await ctx.send(embed=em)
        await user.send('A recipt of a moderator action has been sent to you:', embed=em)

    @commands.command(name='kick', aliases=['boot'])
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def _kick(self, ctx, user: discord.Member, *, reason='None'):
        """Kicks a user

        Params:
        user - user to kick
        reason - {optional} reason for kick
        """

        em = discord.Embed(colour=discord.Colour.orange(),
                           description='Logging Entry - `/kick`\n\nAppeals can be sent in the '
                                       '[verification server](http://discord.gg/JHTyKYA)')
        em.add_field(name='Kicked member', value=f'{user.mention}')
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await user.send('You can appeal by DMing me once you join '
                        'the Auth server by using `/appeal [contents]`.', embed=em)

        toscd = self.bot.get_guild(288455332173316106)
        channel = toscd.get_channel(288467626890362880)

        await channel.send(embed=em)
        await ctx.send(embed=em)
        await user.kick(reason=f'Action by {ctx.author}')

    @commands.command(name='ban')
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def _ban(self, ctx, user: discord.Member, *, reason='None'):
        """Bans a user

        Params:
        user - A member of the discord
        reason - {optional} reason for ban
        """

        em = discord.Embed(colour=discord.Colour.orange(),
                           description='Logging Entry - `/ban`\n\nAppeals can be sent in the '
                                       '[verification server](http://discord.gg/JHTyKYA)')
        em.add_field(name='Banned member', value=f'{user.mention}')
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await user.send('You can appeal by DMing me once you join '
                        'the Auth server by using `/appeal [contents]`', embed=em)
        toscd = self.bot.get_guild(288455332173316106)
        channel = toscd.get_channel(288467626890362880)
        await channel.send(embed=em)
        await user.ban(reason=f'Action by {ctx.author}')
        await ctx.send(embed=em)

    @commands.command(name='mute', aliases=['blackmail', 'bm'])
    @commands.has_any_role('Administrator', 'Senior Moderator', 'Moderator')
    async def _mute(
            self,
            ctx,
            user: discord.Member,
            time: typing.Optional[int]=3600,
            *, reason='None'
    ):
        """Mutes a user.
        
        Params:
        user - A member of the Discord
        time - {optional} in seconds
        reason - {optional} reason for mute
        """

        em = discord.Embed(colour=discord.Colour.orange(),
                           description='Logging Entry - `/mute`\n\nAppeals can be sent to me!')
        em.add_field(name='Muted member', value=f'{user.mention}', inline=True)
        em.add_field(name='Time:', value=f'{time}', inline=True)
        em.add_field(name='Reason:', value=reason)
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()
        em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        toscd = self.bot.get_guild(288455332173316106)
        muted = toscd.get_role(289194167463182337)
        channel = toscd.get_channel(288467626890362880)

        await user.send('You can appeal by DMing me by using `/appeal [contents]`', embed=em)
        await channel.send(embed=em)
        await user.add_roles(muted, reason=f'Action by {ctx.author}')
        await ctx.send(embed=em)
        await __import__('asyncio').sleep(time)
        await user.remove_roles(muted, reason='Unmute.')
        await user.send('You have been unmuted.')

    @commands.command()
    async def appeal(self, ctx, *, contents):
        """You can send an appeal to the mods using this command.
        Please be as detailed as you can in the details.
        """

        em = discord.Embed(colour=discord.Colour.dark_magenta(), description='Appeal Entry')
        em.add_field(name='Member:', value=f'{ctx.author}, ID `{ctx.author.id}`')
        em.add_field(name='Contents:', value=f'{contents}')
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()

        toscd = self.bot.get_guild(288455332173316106)
        channel = toscd.get_channel(297442649168936961)

        await channel.send(embed=em)
        await ctx.author.send('Your appeal was successfully sent.')


def setup(bot):
    bot.add_cog(Moderation(bot))

        em = discord.Embed(colour=discord.Colour.dark_magenta(), description='Appeal Entry')
        em.add_field(name='Member:', value=f'{ctx.author}, ID `{ctx.author.id}`')
        em.add_field(name='Contents:', value=f'{contents}')
        em.set_footer(text='ToS Community Discord', icon_url=ctx.guild.icon_url)
        em.timestamp = datetime.datetime.utcnow()

        toscd = self.bot.get_guild(288455332173316106)
        channel = toscd.get_channel(297442649168936961)

        await channel.send(embed=em)
        await ctx.author.send('Your appeal was successfully sent.')


def setup(bot):
    bot.add_cog(Moderation(bot))
