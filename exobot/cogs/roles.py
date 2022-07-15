import exobot
import discord
from discord.ext import commands


class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        roles_channel = exobot.config['ROLES_CHANNEL'] 
        roles = exobot.config['roles']

        if reaction.message.channel.id != roles_channel:
            return

        for _, roles in roles.items():
            for role_name, emoji in roles.items():

                if reaction.emoji.name != emoji:
                    continue

                selected_role = discord.utils.get(user.guild.roles, name=role_name) 
                await user.add_roles(selected_role)


async def setup(bot):
    await bot.add_cog(Roles(bot), guild=discord.Object(id=929135361735671889))