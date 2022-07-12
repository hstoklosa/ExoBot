import random
import aiohttp
import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        """Responds with a random meme"""

        meme_embed = discord.Embed(
            title = "ExoBot Random Meme",
            description = "Fetched from reddit.com/r/memes",
            colour = discord.Colour.blue()
        )

        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.reddit.com/r/dankmemes/new.json?sort=hothttp://httpbin.org/get') as r:
                response = await r.json()

                meme_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
                meme_embed.set_image(url=response['data']['children'] [random.randint(0, 25)]['data']['url'])

                await ctx.send(embed=meme_embed)

        

async def setup(bot):
    await bot.add_cog(Fun(bot))