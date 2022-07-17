import os
import time
import glob

import discord
import exobot
from discord.ext import commands


# NOTE:
# Discord Token and MySQL credentials can be changed at exobot/config/.env
# Other config values related to the bot can be changed at exobot/config/config.json


print(f"""
    ,------. ,--.   ,--.  ,-----.  ,-----.    ,-----.  ,--------. 
    |  .---'  \  `.'  /  '  .-.  ' |  |) /_  '  .-.  ' '--.  .--' 
    |  `--,    .'    \   |  | |  | |  .-.  \ |  | |  |    |  |    
    |  `---.  /  .'.  \  '  '-'  ' |  '--' / '  '-'  '    |  |    
    `------' '--'   '--'  `-----'  `------'   `-----'     `--'    
                                                                
    ExoBot 1.0
    Powered by Discord.py 2.0
""")



# Setting up the bot

class Bot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.reactions = True
        intents.message_content = True

        super().__init__(
            command_prefix = exobot.config['COMMAND_PREFIX'], 
            help_command = None,  
            intents = intents
        )


    async def on_ready(self):
        print(f"Logged in as {self.user}")

        self.start_time = time.time()

        # bot's status & activity
        await self.change_presence(
            status = discord.Status.online, 
            activity = discord.Game(exobot.config['BOT_STATUS'])
        )

        # NOTE:
        # Loading essential custom emojis
        # Upload your icons to exobot/icons (file name will be the name of the command)
        guild = self.guilds[0]
        guild_emojis = [emoji.name for emoji in guild.emojis]

        icons = glob.glob('exobot/icons/*.png')

        for icon_path in icons:
            emoji_name = os.path.basename(icon_path).replace('.png', '')

            if (emoji_name in guild_emojis):
                continue

            with open(icon_path, 'rb') as img:
                img_byte = img.read()

                await guild.create_custom_emoji(name=emoji_name, image=img_byte)


        # NOTE: Loading each category with reactions
        # 1. Set-up roles and custom emojis on your discord sevrer
        # 2. Configure config.json by creating categories and lisitng each role e.g.: "category" -> "role_name": "emoji_name" 

        roles_channel = self.get_channel(exobot.config['ROLES_CHANNEL'])
        roles = exobot.config['roles']

        for category, roles in roles.items():
            msg_category = await roles_channel.send(f"Category: **{category}**")

            for _, emoji in roles.items():
                emoji_obj = discord.utils.get(roles_channel.guild.emojis, name=emoji)

                if emoji_obj is None:
                    continue

                await msg_category.add_reaction(emoji_obj)


    # overwritten discord method, ties to the setup() method in each cog
    async def setup_hook(self):
        # find cogs folder in ./exobot and load all class files
        for fn in os.listdir('./exobot/cogs'):
            if fn.endswith('.py'):
                await self.load_extension(f"exobot.cogs.{fn[:-3]}")

        await self.load_extension('jishaku') # debugging cog
        await self.tree.sync(guild=discord.Object(id=929135361735671889))



# Initialising the bot

bot = Bot()
bot.run(exobot.env['BOT_TOKEN'])
