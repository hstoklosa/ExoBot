import exobot
import discord
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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


    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            title = 'ExoBot - Help',
            colour = discord.Colour.blue()
        )


        embed.add_field(
            name=':bar_chart: Poll Commands', 
            value=f'**{exobot.config["COMMAND_PREFIX"]}poll [question]** - Create a normal poll \n**{exobot.config["COMMAND_PREFIX"]}closepoll [poll_id]** - Disables an active poll', 
            inline = False)    
            
        embed.add_field(
            name=':mag_right: Ranking Commands', 
            value=f'**{exobot.config["COMMAND_PREFIX"]}rank** - Shows your current rank and experience points \n**{exobot.config["COMMAND_PREFIX"]}top [places]** - Shows the first x places', 
            inline = False)

        embed.add_field(
            name=':musical_keyboard: Music Commands', 
            value=f'**{exobot.config["COMMAND_PREFIX"]}join** - Bot joins your channel \n**{exobot.config["COMMAND_PREFIX"]}leave** - Bot leaves your channel \n**{exobot.config["COMMAND_PREFIX"]}yt [link]** - Plays a song from the youtube link \n**{exobot.config["COMMAND_PREFIX"]}volume [amount]** - Sets volume to specified amount', 
            inline = False)

        # await ctx.send(embed=embed)
        await ctx.reply(embed=embed)



def setup(bot):
    bot.add_cog(General(bot))