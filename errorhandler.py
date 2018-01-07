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
        await ctx.bot.say(unkown, embed=error)
      else:
        print('Ignoring exception in command {}'.format(ctx.command), file = sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    
def setup(bot):
  bot.add_cog(Error)