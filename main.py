import time
import os


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

        # bot's avatar & status
        with open('./exobot/assets/avatar.jpg', 'rb') as img:
            await self.user.edit(avatar=img.read())

        await self.change_presence(
            status = discord.Status.online, 
            activity = discord.Game(exobot.config['BOT_STATUS'])
        )


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