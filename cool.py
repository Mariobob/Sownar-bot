import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback


prefix='s.'
bot=commands.Bot(command_prefix=prefix)

class Cool():
    print('random loaded')
    print('------')

    @bot.command(pass_context = True)
    async def rand(ctx):
        await ctx.bot.say("I am working!")
        
    @bot.command(pass_context = True)
    async def say(ctx, *, echo: str):
      await ctx.bot.say(echo)
    
    @bot.command(pass_context = True)
    async def dog(ctx):
      await ctx.bot.say('https://random.dog/')

def setup(bot):
    bot.add_cog(Cool)
