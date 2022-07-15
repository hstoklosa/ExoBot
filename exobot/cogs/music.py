import queue
import asyncio
import youtube_dl
import discord
from discord import app_commands
from discord.ext import commands


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = queue.Queue()


    @app_commands.command(name='join', description='Bot joins your voice channel.')
    async def join(self, ctx):
        channel = ctx.user.voice.channel
        vc = ctx.guild.voice_client

        if vc is not None:
            return await vc.move_to(channel)        

        return await channel.connect()


    @app_commands.command(name='leave', description='Bot leave its current voice channel.')
    async def leave(self, ctx):
        return await ctx.guild.voice_client.disconnect()


    @app_commands.command(name='yt', description='Plays a song from a youtube link.')
    async def yt(self, ctx, *, url: str):
        vc = ctx.guild.voice_client

        async with ctx.channel.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            if (vc.is_playing()):
                self.queue.put(player)
                return await ctx.response.send_message(f'Added to queue: {player.title}')

            vc.play(player, after=lambda e: self.play_next(vc))

        await ctx.response.send_message(f'Now playing: {player.title}')

    def play_next(self, vc):
        if self.queue.empty():
            return vc.stop()

        next_player = self.queue.get()
        vc.play(next_player, after=lambda e: self.play_next(vc))


    @app_commands.command(name='pause', description='Pauses the voice client.')
    async def pause(self, ctx):
        return ctx.guild.voice_client.pause()


    @app_commands.command(name='resume', description='Resumes the voice client.')
    async def resume(self, ctx):
        return ctx.guild.voice_client.resume()
        

    @app_commands.command(name='volume', description='Changes the volume to the specified amount.')
    async def volume(self, ctx, volume: int):
        vc = ctx.guild.voice_client

        if vc is None:
            return await ctx.response.send_message("Not connected to a voice channel.")

        vc.source.volume = volume / 100
        await ctx.response.send_message(f"Changed volume to {volume}%")



async def setup(bot):
    await bot.add_cog(Music(bot), guild=discord.Object(id=929135361735671889))