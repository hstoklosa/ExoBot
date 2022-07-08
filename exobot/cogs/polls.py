import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))

import discord
import shortuuid
from discord import ui
from discord.ext import commands, menus
from managers.database import db, cursor


# listpolls - Menu with pagination

class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        bot = menu.ctx.bot
        embed = discord.Embed(
            title = "Polls Overview",
            description = f"Page {menu.current_page}/3",
            color = discord.Colour.random()
        )


        for page in entries:
            channel = await bot.fetch_channel(page['channel'])
            message = await channel.fetch_message(page['message'])

            # print(channel, message)

            embed.add_field(
                name = f"ID: {page['id']}",
                value = f"[{page['question']}]({message.jump_url})", 
                inline = False
            )

        embed.set_footer(text=f"Requested by {menu.ctx.author}")
        return embed


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None


    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)


    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)

        if 'view' not in value:
            value.update({'view': self})

        return value


    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author


    # This is extremely similar to Custom MenuPages(I will not explain these)
    @ui.button(emoji='⏮', style=discord.ButtonStyle.blurple)
    async def first_page(self, button, interaction):
        await self.show_page(0)


    @ui.button(emoji='⏭', style=discord.ButtonStyle.blurple)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)


    @ui.button(emoji='◀', style=discord.ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)


    @ui.button(emoji='▶', style=discord.ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)


    @ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()



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

    @commands.command()
    async def listpolls(self, ctx):
        cursor.execute("SELECT * FROM polls")
        polls = cursor.fetchall()

        formatter = MySource(polls, per_page=3)
        menu = MyMenuPages(formatter)

        await menu.start(ctx)



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