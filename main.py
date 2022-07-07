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
    exobot.cogs.roles.setup(bot)

    await bot.change_presence(
        status = discord.Status.online, 
        activity = discord.Game(exobot.config['BOT_STATUS'])
    )

    # Loading roles channel
    roles_channel = bot.get_channel(exobot.config['ROLES_CHANNEL'])
    roles = exobot.config['roles']

    # NOTE:
    # Loading each category with its roles
    # Set-up roles and custom emojis on your discord sevrer
    # Configure config.json by creating categories and lisitng each role e.g.: "category" -> "role_name": "emoji_name" 

    for category, roles in roles.items():
        msg_category = await roles_channel.send(f"Category: **{category}**")

        for _, emoji in roles.items():
            emoji_obj = discord.utils.get(roles_channel.guild.emojis, name=emoji)

            if emoji_obj is None:
                continue

            await msg_category.add_reaction(emoji_obj)



# Initialising the bot
if __name__ == '__main__':

    try:
        bot.run(env_config['BOT_TOKEN'])
        
    except Exception as e:
        print("Error: Failed to connect with the Discord API. Please check your discord token!")
        exit(1)

