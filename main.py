import discord
from discord.ext import commands

print(f"""
    ,------. ,--.   ,--.  ,-----.  ,-----.    ,-----.  ,--------. 
    |  .---'  \  `.'  /  '  .-.  ' |  |) /_  '  .-.  ' '--.  .--' 
    |  `--,    .'    \   |  | |  | |  .-.  \ |  | |  |    |  |    
    |  `---.  /  .'.  \  '  '-'  ' |  '--' / '  '-'  '    |  |    
    `------' '--'   '--'  `-----'  `------'   `-----'     `--'    
                                                                
    ExoBot 1.0
    Powered by discord.py
""")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot('$', intents=intents)

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

if __name__ == '__main__':
    bot.run()
