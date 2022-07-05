from discord.ext import commands

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(992418879580147722)

        await channel.send(f"Welcome {member.mention} to the server!")


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(992424825391960095)

        if (not channel):
            return

        await channel.send(f"Bye {member.mention}! See you next time!")

def setup(bot):
    bot.add_cog(General(bot))