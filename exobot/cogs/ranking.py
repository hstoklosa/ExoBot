import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

import discord
from discord.ext import commands
from managers.database import db, cursor


class Ranking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            await self.add_experience(message.author)
            await self.level_up(message.author, message)


    async def add_experience(self, user):
            cursor.execute("UPDATE users SET experience = experience + 6 WHERE user_id = %s", (user.id, ))
            db.commit()

            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user.id, ))
            db_user = cursor.fetchall()[0]
            print(db_user)


    async def level_up(self, user, message):
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user.id, ))
        db_user = cursor.fetchall()[0]

        experience = db_user['experience']
        lvl_start = db_user['level']
        lvl_end = int(experience ** (1 / 4))

        if lvl_start < lvl_end:
            await message.channel.send(f':tada:  {user.mention} has reached level {lvl_end}. Congrats!  :tada:')
            
            cursor.execute("UPDATE users SET level = %s WHERE user_id = %s", (lvl_end, user.id))
            db.commit()


    @commands.command()    
    async def rank(self, ctx, member: discord.Member = None):
        if member == None:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (ctx.author.id, ))
            db_user = cursor.fetchall()[0]

            return await ctx.send(f"{ctx.author.mention} You are at level {db_user['level']}!")

        cursor.execute("SELECT * FROM users WHERE user_id = %s", (member.id, ))
        db_user = cursor.fetchall()[0]

        await ctx.send(f"{member.mention} is at level {db_user['level']}!")


    @commands.command()
    async def top(self, ctx, amount = 5):
        cursor.execute("SELECT * FROM users ORDER BY level DESC LIMIT %s", (amount, ))
        users = cursor.fetchall()

        ranking_string = f">>> :chart_with_upwards_trend:  Top {amount} Users: \n"

        for idx, user in enumerate(users):
            dc_user = await self.bot.fetch_user(user['user_id'])
            level, exp = user['level'], user['experience']

            ranking_string += f"\n{idx + 1}. **{dc_user.display_name}** (Lvl. {level} - Exp. {exp})"

        await ctx.send(ranking_string)


def setup(bot):
    bot.add_cog(Ranking(bot))