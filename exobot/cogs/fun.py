import random
import aiohttp
import discord
from discord import app_commands, ui
from discord.ext import commands


class MyMenu(ui.View):

    def __init__(self):
        super().__init__()
        
        self.choice = None


    @ui.button(emoji='🤜')
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = 'rock'

    @ui.button(emoji='🖐️')
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = 'paper'

    @ui.button(emoji='✌️')
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = 'scissors'



class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='meme', description='Responds with a random meme')
    async def meme(self, ctx):

        meme_embed = discord.Embed(
            title = "ExoBot Random Meme",
            description = "Fetched from reddit.com/r/memes",
            colour = discord.Colour.blue()
        )

        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/new.json?sort=hothttp://httpbin.org/get') as r:
                response = await r.json()

                meme_embed.set_footer(text=f"Requested by {ctx.user}", icon_url=ctx.user.avatar.url)
                meme_embed.set_image(url=response['data']['children'] [random.randint(0, 25)]['data']['url'])

                await ctx.response.send_message(embed=meme_embed)

        
    @app_commands.command(name='rps', description='Challange the bot/user to a game of Rock, Paper, Scissors.')
    async def rps(self, ctx):
        print('hello world')
        await ctx.response.send_message('Hello World')
        
        view = MyMenu()
        await ctx.response.send_message(view=view)


async def setup(bot):
    await bot.add_cog(Fun(bot), guild=discord.Object(id=929135361735671889))