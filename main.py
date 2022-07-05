import json
import discord
from discord.ext import commands
from dotenv import dotenv_values

import exobot

print(f"""
    ,------. ,--.   ,--.  ,-----.  ,-----.    ,-----.  ,--------. 
    |  .---'  \  `.'  /  '  .-.  ' |  |) /_  '  .-.  ' '--.  .--' 
    |  `--,    .'    \   |  | |  | |  .-.  \ |  | |  |    |  |    
    |  `---.  /  .'.  \  '  '-'  ' |  '--' / '  '-'  '    |  |    
    `------' '--'   '--'  `-----'  `------'   `-----'     `--'    
                                                                
    ExoBot 1.0
    Powered by discord.py
""")


# Loading env config

env_config = dotenv_values(".env")


# Initialising the bot with the intents

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(exobot.config['COMMAND_PREFIX'], intents=intents)


def init():

    @bot.event
    async def on_ready():
        print(f'Logged on as {bot.user}!')

        # Loading cogs

        exobot.cogs.general.setup(bot)

    bot.run(env_config['DISCORD_TOKEN'])

if __name__ == '__main__':

    init()