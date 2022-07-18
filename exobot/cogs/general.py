import os
import glob

import exobot
import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        # NOTE: Loading custom emojis
        # Upload your icons to exobot/icons (file name will be the name of the command)

        guild = self.bot.guilds[0]
        guild_emojis = [emoji.name for emoji in guild.emojis]

        icons = glob.glob('exobot/assets/icons/*.png')

        for icon_path in icons:
            emoji_name = os.path.basename(icon_path).replace('.png', '')

            if emoji_name in guild_emojis:
                continue

            with open(icon_path, 'rb') as img:
                img_byte = img.read()

                await guild.create_custom_emoji(name=emoji_name, image=img_byte)


        # NOTE: Loading each category with reactions
        # 1. Set-up roles and custom emojis on your discord sevrer
        # 2. Configure config.json by creating categories and lisitng each role e.g.: "category" -> "role_name": "emoji_name" 

        roles_channel = self.bot.get_channel(exobot.config['ROLES_CHANNEL'])
        roles = exobot.config['roles']

        for category, roles in roles.items():
            msg_category = await roles_channel.send(f"Category: **{category}**")

            for _, emoji in roles.items():
                emoji_obj = discord.utils.get(roles_channel.guild.emojis, name=emoji)

                if emoji_obj is None:
                    continue

                await msg_category.add_reaction(emoji_obj)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(exobot.config['WELCOME_CHANNEL'])

        if not channel:
            return

        await channel.send(f"Welcome {member.mention} to the server!")


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(exobot.config['GOODBYE_CHANNEL'])

        if not channel:
            return

        await channel.send(f"Bye {member.mention}! See you next time!")


    @app_commands.command(name='help', description='Lost? This is the command you\'re looking for.') 
    async def help(self, ctx):
        prefix = exobot.config["COMMAND_PREFIX"]

        embed = discord.Embed(
            title = 'ExoBot - Help',
            colour = discord.Colour.blue()
        )


        embed.add_field(
            name = ':bar_chart: Poll Commands', 
            value = f'**{prefix}poll [question]** - Create a normal poll \n**{prefix}closepoll [poll_id]** - Deactivates an active poll \n**{prefix}listpolls** - Displays all polls', 
            inline = False
        )    
            
        embed.add_field(
            name = ':mag_right: Ranking Commands', 
            value = f'**{prefix}rank [optional: user mention]** - Shows user\'s current rank and experience points \n**{prefix}top [places]** - Shows the first x places', 
            inline = False
        )

        embed.add_field(
            name = ':musical_keyboard: Music Commands', 
            value = f'**{prefix}join** - Bot joins your channel \n**{prefix}leave** - Bot leaves your channel \n**{prefix}yt [link]** - Plays a song from the youtube link \n**{prefix}pause** - Pauses the song \n**{prefix}resume** - Resumes the song \n**{prefix}volume [amount]** - Sets volume to specified amount', 
            inline = False
        )

        embed.add_field(
            name = ':information_source: Info Commands',
            value = f'**{prefix}server** - Displays server information \n**{prefix}roles** - Displays all roles including the amount of members \n**{prefix}user [optional: user mention]** - Displays information about the user \n**{prefix}avatar [optional: user mention]** - Displays the avatar of the user \n**{prefix}uptime** - Shows the bot\'s uptime \n**{prefix}ping** - Shows the bot\'s ping',
            inline = False
        )

        embed.add_field(
            name = ':joy: Fun Commands',
            value = f'**{prefix}meme** - Sends a random meme to the channel',
            inline = False
        )


        await ctx.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(General(bot), guild=discord.Object(id=929135361735671889))