import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import requests

prefix='s.'
bot=commands.Bot(command_prefix=prefix)

class Fun():
    print('Fun loaded')
    print('------')

    @bot.command(pass_context = True)
    async def fun(ctx):
        await ctx.bot.say("I am working!")

def setup(bot):
    bot.add_cog(Fun)
