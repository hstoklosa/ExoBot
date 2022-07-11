import queue
import asyncio
import youtube_dl
import discord
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


    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)        

        return await channel.connect()


    @commands.command()
    async def leave(self, ctx):
        return await ctx.voice_client.disconnect()


    @commands.command()
    async def yt(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

            if (ctx.voice_client.is_playing()):
                self.queue.put(player)
                return await ctx.send(f'Added to queue: {player.title}')

            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))

        await ctx.send(f'Now playing: {player.title}')

    def play_next(self, ctx):
        if self.queue.empty():
            return ctx.voice_client.stop()

        next_player = self.queue.get()
        ctx.voice_client.play(next_player, after=lambda e: self.play_next(ctx))


    @commands.command()
    async def pause(self, ctx):
        return ctx.voice_client.pause()


    @commands.command()
    async def resume(self, ctx):
        return ctx.voice_client.resume()
        

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")



async def setup(bot):
    await bot.add_cog(Music(bot))