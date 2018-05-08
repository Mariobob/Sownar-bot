import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback

prefix=["s.", "s>", "s/"]
bot=commands.Bot(command_prefix=prefix)
unkown = discord.Object("399410266519109632")
other = discord.Object("399410308587716609")

class Error():
    print('ErrorHandler loaded')
    print('------')
    
    
    @bot.event
    async def on_command_error(error, ctx):
      if isinstance(error, commands.CommandNotFound):
        error=discord.Embed(title=":warning: Error", description="Command attempted: `{}`".format(ctx.message.content))
        error.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        error.set_author(name=ctx.message.server.name, icon_url=ctx.message.server.icon_url)
        await ctx.bot.send_message(unkown, embed=error)
      elif isinstance(error, command.CommandOnCooldown):
        await ctx.bot.say(error)
      else:
#        print('Ignoring exception in command {}'.format(ctx.message.content))
#        traceback.print_exception(type(error), error, error.__traceback__)
        embed = discord.Embed(title=":warning: Error!", description="Command Error: `s.{0}`\n{1}: {2}".format(ctx.command, type(error).__name__, error), color=0xff0000)
        embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        embed.set_author(name=ctx.message.server.name, icon_url=ctx.message.server.icon_url)
        await ctx.bot.send_message(other, embed= embed)

    
def setup(bot):
  bot.add_cog(Error)
