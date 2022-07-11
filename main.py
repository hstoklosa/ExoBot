import os
import glob
import datetime, time

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



@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

    # NOTE: Uptime calculations
    bot.start_time = time.time()

    # Changing bot's status & activity
    await bot.change_presence(
        status = discord.Status.online, 
        activity = discord.Game(exobot.config['BOT_STATUS'])
    )


    guild = bot.guilds[0]

    # Loading essential custom emojis
    # NOTE: Upload your icons to exobot/icons (file name will be the name of the command)
    icons = glob.glob('exobot/icons/*.png')
    guild_emojis = [emoji.name for emoji in guild.emojis]

    for icon_path in icons:
        emoji_name = os.path.basename(icon_path).replace('.png', '')

        if (emoji_name in guild_emojis):
            continue

        with open(icon_path, 'rb') as img:
            img_byte = img.read()

            await guild.create_custom_emoji(name=emoji_name, image=img_byte)



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



    # Loading cogs    
    await exobot.cogs.general.setup(bot)
    await exobot.cogs.ranking.setup(bot)
    await exobot.cogs.polls.setup(bot)
    await exobot.cogs.music.setup(bot)
    await exobot.cogs.roles.setup(bot)
    await exobot.cogs.info.setup(bot)
    await exobot.cogs.fun.setup(bot)




# Initialising the bot
if __name__ == '__main__':

    try:
        bot.run(env_config['BOT_TOKEN'])
    except Exception as e:
        print("Error: Failed to connect with the Discord API. Please check your discord token!")
        exit(1)

