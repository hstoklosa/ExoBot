import discord
from discord import app_commands
from discord.ext import commands
from exobot import env
from exobot.managers.osu import Osu


class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.osu_client = Osu(env['CLIENT_ID'], env['CLIENT_SECRET'])


    @app_commands.command(name='osu', description='Displays the specified user\'s statistics on osu!.')
    async def osu(self, ctx, user:str):
        user = await self.osu_client.get_user(user)

        emoji_obj = discord.utils.get(ctx.guild.emojis, name='osu')

        osu_embed = discord.Embed(
            title = f'{emoji_obj} {user.username} on osu!',
            colour = discord.Colour.blue()
        )

        osu_embed.set_thumbnail(url=user.avatar_url)
        osu_embed.set_footer(text=f'Requested by {ctx.user}', icon_url=ctx.user.avatar.url)

        # 1st row

        osu_embed.add_field(
            name = "ID",
            value = user._id,
            inline = True
        )

        osu_embed.add_field(
            name = "Username",
            value = user.username,
            inline = True
        )

        osu_embed.add_field(
            name = "Country",
            value = user.country,
            inline = True
        )

        # 2nd row

        osu_embed.add_field(
            name = "Level",
            value = user.current_level + (user.progress / 100),
            inline = True 
        )

        percent = int(13 * (user.progress / 100))
        bar = '█' * percent + '░' * (13 - percent)

        osu_embed.add_field(
            name = "Progress",
            value = bar,
            inline = True
        )

        osu_embed.add_field( 
            name = "\u200b",
            value = "\u200b",
            inline = True
        ) # empty field to make the next row start on a new line

        # 3rd row and so on... 

        osu_embed.add_field(
            name = "Accuracy",
            value = user.accuracy,
            inline = True
        )

        osu_embed.add_field(
            name = "Global/Country Rank",
            value = f'#{user.global_rank} / #{user.country_rank}',
            inline = True
        )

        osu_embed.add_field(
            name = "Playcount",
            value = user.playcount,
            inline = True
        )

        osu_embed.add_field(
            name = "PP",
            value = user.pp_raw,
            inline = True
        )

    

        await ctx.response.send_message(embed=osu_embed)



async def setup(bot):
    await bot.add_cog(Misc(bot), guild=discord.Object(id=929135361735671889))