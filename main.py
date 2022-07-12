import os
import asyncio
import discord
from discord.ext import commands
import exobot
from dotenv import dotenv_values


# NOTE:
# Discord Token and MySQL credentials can be changed in the .env file.
# Other config values related to the bot can be changed in the config.json file.


print(f"""
    ,------. ,--.   ,--.  ,-----.  ,-----.    ,-----.  ,--------. 
    |  .---'  \  `.'  /  '  .-.  ' |  |) /_  '  .-.  ' '--.  .--' 
    |  `--,    .'    \   |  | |  | |  .-.  \ |  | |  |    |  |    
    |  `---.  /  .'.  \  '  '-'  ' |  '--' / '  '-'  '    |  |    
    `------' '--'   '--'  `-----'  `------'   `-----'     `--'    
                                                                
    ExoBot 1.0
    Powered by Discord.py 2.0
""")


# Loading env config

env_config = dotenv_values(".env")


# Setting up intents

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(exobot.config['COMMAND_PREFIX'], help_command=None, intents=intents)


async def load_extensions():
    await bot.load_extension('jishaku')

    # Loading cogs
    for filename in os.listdir("./exobot/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"exobot.cogs.{filename[:-3]}")


# Initialising the bot

async def main():
    async with bot:
        await load_extensions()
        await bot.start(env_config['BOT_TOKEN'])

asyncio.run(main())