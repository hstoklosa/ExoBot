import exobot
import discord
from discord.ext import commands
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
    Powered by discord.py
""")


# Loading env config

env_config = dotenv_values(".env")


# Setting up intents

intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(exobot.config['COMMAND_PREFIX'], intents=intents)

# for overriding the default help command
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

    # Loading cogs
    exobot.cogs.general.setup(bot)
    exobot.cogs.ranking.setup(bot)
    exobot.cogs.polls.setup(bot)
    exobot.cogs.music.setup(bot)


# Initialising the bot
if __name__ == '__main__':

    try:
        bot.run(env_config['DISCORD_TOKEN'])
    except Exception as e:
        print("Failed to connect with the Discord API. Please check your discord token.")
        exit(1)

