import exobot
import discord
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
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


        await ctx.send(embed=server_embed)

async def setup(bot):
    await bot.add_cog(Info(bot))