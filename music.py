import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
from discord.voice import VoiceClient
if not discord.opus.is_loaded():
  discord.opus.load_opus('opus')

prefix='s.'
bot=commands.Bot(command_prefix=prefix)


class Music():
    print('Music loaded')
    print('------')

    async def create_voice_client(channel):
        voice = await ctx.bot.join_voice_channel(channel)
        state = ctx.bot.get_voice_state(channel.server)
        state.voice = voice
    
    def get_voice_state(server):
        state = ctx.bot.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            ctx.bot.voice_states[server.id] = state

        return state


    @bot.command(pass_context=True)
    async def summon(ctx):
      summon_channel=ctx.message.author.voice_channel
      if summon_channel is None:
        summon_error = discord.Embed(title=":warning: Error!",description="You don't seem to be in a voice channel",color=0xff0000)
        await ctx.bot.say(embed=summon_error)
      else:
        state = ctx.bot.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await ctx.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)
      return True
        
    @bot.command(pass_context=True, no_pm=True)
    async def play(ctx, *, song: str):
      state = ctx.bot.get_voice_state(ctx.message.server)
      opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        
      if state.voice is None:
        success = await ctx.invoke(ctx.bot.summon)
        loading_song = discord.Embed(title="The song is being loaded", description = "Thank you for your patience")
        await ctx.bot.say(embed=loading_song)
        
      try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except:
            fmt = 'An error occurred while processing this request'
            await ctx.bot.send_message(ctx.message.channel, fmt)
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await ctx.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)

    @bot.command(pass_context=True, no_pm=True)
    async def stop(ctx):
        server = ctx.message.server
        state = ctx.bot.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del ctx.bot.voice_states[server.id]
            await state.voice.disconnect()
            await ctx.bot.say("Cleared the queue and disconnected from voice channel ")





def setup(bot):
    bot.add_cog(Music)
