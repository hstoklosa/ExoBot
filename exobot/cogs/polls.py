import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

import discord
import shortuuid
from discord.ext import commands
from managers.database import db, cursor



class Polls(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def poll(self, ctx, question):
        poll_id = shortuuid.ShortUUID().random(length=10)

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )

        embed.add_field(name='Question', value=question, inline = False)    
        embed.add_field(name='Choices', value='👍 Yes \n\n 👎 No', inline = False)
        embed.add_field(name='Settings', value='None', inline = False)
        embed.add_field(name='Status', value=":green_circle: Active", inline = False)
        embed.set_footer(text=f'Poll ID: {poll_id}')

        sent_message = await ctx.send(embed=embed)

        
        # Add reactions for voting
        await sent_message.add_reaction('👍')
        await sent_message.add_reaction('👎')

        cursor.execute("INSERT INTO polls (id, user_id, question, channel, message) VALUES (%s, %s, %s, %s, %s)", (poll_id, ctx.author.id, question, ctx.channel.id, sent_message.id))
        db.commit()


    @commands.command()
    async def closepoll(self, ctx, poll_id):
        cursor.execute("SELECT * FROM polls WHERE id = %s", (poll_id, ))
        poll = cursor.fetchone()

        if poll is None:
            return
    

        # Changing status of the poll in the database
        cursor.execute("UPDATE polls SET status = %s WHERE id = %s", ('0', poll_id))
        db.commit()
        
        # Retrieving the message
        channel = await self.bot.fetch_channel(poll['channel'])
        message = await channel.fetch_message(poll['message'])
        
        # Assign changes to the embed
        embed_dict = message.embeds[0].to_dict()
        embed_dict['color'] = discord.Colour.red().value

        embed = discord.Embed.from_dict(embed_dict)
        embed.set_field_at(3, name='Status', value=':red_circle: Disabled', inline=True)

        await message.edit(embed=embed)

        close_embed = discord.Embed(
            title = 'Poll closed',
            description = f'The poll with ID **{poll["id"]}** has been closed! \nVotes will no longer be accepted.',
            colour = discord.Colour.blue()
        )

        #components=[Button(style=ButtonStyle.red, label="60 million years ago", custom_id="button1", disabled = True), Button(style=ButtonStyle.red, label="65 million years ago", custom_id="button2")]

        await ctx.send(embed=close_embed)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user = await self.bot.fetch_user(payload.user_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        choices = [":thumbsup:", ":thumbsdown:"]

        cursor.execute("SELECT * FROM polls WHERE status = %s", ('0', ))
        disabled_polls = cursor.fetchall()

        for poll in disabled_polls:
            
            # ensure the message is a poll
            if poll['channel'] == str(payload.channel_id) and poll['message'] == str(payload.message_id):
                
                # only the bot can react
                if user.id != self.bot.user.id and payload.emoji.name not in choices:
                    await reaction.remove(payload.member)



async def setup(bot):
    await bot.add_cog(Polls(bot))