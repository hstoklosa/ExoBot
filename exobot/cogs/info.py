import datetime, time

import exobot
import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name='server', description='Displays information about the server')
    async def server(self, ctx):
        """Displays information about the server"""
        guild = ctx.guild

        server_embed = discord.Embed(
            title = guild.name,
            colour = discord.Colour.blue()
        )

        server_embed.add_field(
            name = ":id: **Server ID:**",
            value = guild.id,
            inline = True
        )

        server_embed.add_field(
            name = "<:crown:995719728498757672> **Server Owner:**",
            value = guild.owner.mention,
            inline = True
        )

        server_embed.add_field(
            name = ":calendar: **Created on:**",
            value = exobot.utils.format_date(guild.created_at),
            inline = True
        )


        online_members = exobot.utils.online_members(guild)

        server_embed.add_field(
            name = f"<:members:995719729593471077> Members ({len(guild.members)})",
            value = f"Online: **{online_members}**",
            inline = True

        )

        server_embed.add_field(
            name = f"<:chat:995728759980314715> Channels ({len(guild.channels)})",
            value = f"Text: **{len(guild.text_channels)}** \nVoice: **{len(guild.voice_channels)}**",
            inline = True
        )


        roles = await guild.fetch_roles()

        server_embed.add_field(
            name = f":lock:** Roles ({len(roles)})**",
            value = f"To see a list with all roles use **{exobot.config['COMMAND_PREFIX']}roles**",
            inline = True 
        )


        await ctx.response.send_message(embed=server_embed)


    @app_commands.command(name='roles', description='Displays a list of all guild roles')
    async def roles(self, ctx):
        roles = ctx.guild.roles

        roles_embed = discord.Embed(
            title = "ExoBot Roles",
            colour = discord.Colour.blue()
        )

        for role in roles:
            name, members = role.name, len(role.members)

            roles_embed.add_field(
                name = "\u200b",
                value = f"{name} (**{members}** members) ",
                inline = False
            )

        await ctx.response.send_message(embed=roles_embed)


    @app_commands.command(name='user', description='Displays information about the specified user')
    async def user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.user

        user_embed = discord.Embed(
            colour = discord.Colour.blue()
        )


        user_embed.add_field(
            name = "Joined Discord:",
            value = exobot.utils.format_date(member.created_at),
            inline = False
        )

        user_embed.add_field(
            name = "Joined Server:",
            value = exobot.utils.format_date(member.joined_at),
            inline = False
        )

        user_embed.set_thumbnail(url=member.avatar.url)
        user_embed.set_footer(text=member, icon_url=member.avatar.url)

        await ctx.response.send_message(embed=user_embed)


    @app_commands.command(name='avatar', description='Displays specified user\'s avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.user

        avatar_embed = discord.Embed(
            description = f"[Avatar URL]({member.avatar.url}])",
            colour = discord.Colour.blue()
        )

        avatar_embed.set_author(name=member, icon_url=member.avatar.url)
        avatar_embed.set_footer(text=f"Requested by {ctx.user}", icon_url=ctx.user.avatar.url)

        avatar_embed.set_image(url=member.avatar.url)

        await ctx.response.send_message(embed=avatar_embed)



    @app_commands.command(name='ping', description='Bot latency')
    async def ping(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"My ping is {self.bot.latency}ms")


    @app_commands.command(name='uptime', description='Shows how long the bot has been running')
    async def uptime(self, ctx):
        start_time = self.bot.start_time

        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))

        uptime_embed = discord.Embed(
            title = "ExoBot Uptime",
            description = uptime,
            colour = discord.Colour.blue()
        )

        uptime_embed.set_footer(text=f'Requested by {ctx.user}', icon_url=ctx.user.avatar.url)

        await ctx.response.send_message(embed=uptime_embed)



async def setup(bot):
    await bot.add_cog(Info(bot), guild=discord.Object(id=929135361735671889))