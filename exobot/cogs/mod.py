import discord
from discord.ext import commands

class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def mute(self, ctx, member: discord.Member, reason):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, "Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")

            for channel in guild.channels:
                channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role, reason=reason)

        muted_embed = discord.Embed(
            title = "ExoBot Mute",
            description = f"User {member.name} has been muted! \n**Reason:** {reason}",
            colour = discord.Colour.blue()
        )

        await ctx.send(embed=muted_embed)


    async def unmute(self, ctx, member: discord.Member, reason):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, "Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")

            for channel in guild.channels:
                channel.set_permissions(muted_role, speak=False, send_messages=False)

            return

        await member.remove_roles(muted_role)

        

async def setup(bot):
    await bot.add_cog(Mod(bot), guild=discord.Object(id=929135361735671889))