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

def setup(bot):
  bot.add_cog(modmail)

class ModMail():
    print('ModMail loaded')
    print('------')
