import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='s.')
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')
    

class VoiceEntry:
    def __init__(ctx, message, player):
        ctx.requester = message.author
        ctx.channel = message.channel
        ctx.player = player

    def __str__(ctx):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = ctx.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(ctx.player, ctx.requester)

class VoiceState:
    def __init__(ctx, bot):
        ctx.current = None
        ctx.voice = None
        ctx.bot = bot
        ctx.play_next_song = asyncio.Event()
        ctx.songs = asyncio.Queue()
        ctx.skip_votes = set() # a set of user_ids that voted
        ctx.audio_player = ctx.bot.loop.create_task(ctx.audio_player_task())

    def is_playing(ctx):
        if ctx.voice is None or ctx.current is None:
            return False

        player = ctx.current.player
        return not player.is_done()

    @property
    def player(ctx):
        return ctx.current.player

    def skip(ctx):
        ctx.skip_votes.clear()
        if ctx.is_playing():
            ctx.player.stop()

    def toggle_next(ctx):
        ctx.bot.loop.call_soon_threadsafe(ctx.play_next_song.set)

    async def audio_player_task(ctx):
        while True:
            ctx.play_next_song.clear()
            ctx.current = await ctx.songs.get()
            await ctx.bot.send_message(ctx.current.channel, 'Now playing ' + str(ctx.current))
            ctx.current.player.start()
            await ctx.play_next_song.wait()

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(ctx, bot):
        ctx.bot = bot
        ctx.voice_states = {}

    def get_voice_state(ctx, server):
        state = ctx.voice_states.get(server.id)
        if state is None:
            state = VoiceState(ctx.bot)
            ctx.voice_states[server.id] = state

        return state

    async def create_voice_client(ctx, channel):
        voice = await ctx.bot.join_voice_channel(channel)
        state = ctx.get_voice_state(channel.server)
        state.voice = voice

    def __unload(ctx):
        for state in ctx.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    ctx.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await ctx.create_voice_client(channel)
        except discord.ClientException:
            await ctx.bot.say('Already in a voice channel...')
        except discord.InvalidArgument:
            await ctx.bot.say('This is not a voice channel...')
        else:
            await ctx.bot.say('Ready to play audio in ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await ctx.bot.say('You are not in a voice channel.')
            return False

        state = ctx.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await ctx.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = ctx.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(ctx.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await ctx.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await ctx.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(ctx, value : int):
        """Sets the volume of the currently playing song."""

        state = ctx.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await ctx.bot.say('Set the volume to {:.0%}'.format(player.volume))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(ctx):
        """Pauses the currently played song."""
        state = ctx.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(ctx):
        """Resumes the currently played song."""
        state = ctx.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = ctx.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del ctx.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = ctx.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await ctx.bot.say('Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await ctx.bot.say('Requester requested skipping song...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await ctx.bot.say('Skip vote passed, skipping song...')
                state.skip()
            else:
                await ctx.bot.say('Skip vote added, currently at [{}/3]'.format(total_votes))
        else:
            await ctx.bot.say('You have already voted to skip this song.')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(ctx):
        """Shows info about the currently played song."""

        state = ctx.get_voice_state(ctx.message.server)
        if state.current is None:
            await ctx.bot.say('Not playing anything.')
        else:
            skip_count = len(state.skip_votes)
            await ctx.bot.say('Now playing {} [skips: {}/3]'.format(state.current, skip_count))

def setup(bot):
bot.add_cog(music)
