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


env_config = dotenv_values(".env")


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot('$', intents=intents)

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

    exobot.cogs.general.setup(bot)

if __name__ == '__main__':
    bot.run(env_config['DISCORD_TOKEN'])
