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

class random():
    print('random loaded')
    print('------')

    @bot.command(pass_context = True)
    async def rand(ctx):
        await ctx.bot.say("I am working!")

def setup(bot):
    bot.add_cog(random)
