import json
import aiohttp
import asyncio
import os
import requests
import discord
from discord.ext import commands

with open("token_file2.pk1", "r") as token_file2:
  dbl = json.load(token_file2)
bot=commands.Bot(command_prefix='s.')
ownerids=['221381001476046849', '221263215496134656']

url = "https://discordbots.org/api/bots/" + '375370278810681344' + "/stats"
headers = {"Authorization" : dbl}

class botsorgapi():
  print('DBL API Loaded')
  
  @bot.command(pass_context = True, hidden = True)
  async def dblAPIload(ctx):
    if ctx.message.author.id not in ownerids:
      pass
    else:
      try:
        payload = {"server_count"  : len(ctx.bot.servers)}
        requests.post(url, data=payload, headers=headers)
        await ctx.bot.say(":white_check_mark: Succes!")
      except Exception as e:
              embed = discord.Embed(title=":warning: Error!", description="Failed loading {0}\n{1}: {2}".format(extension, type(e).__name__, e), color=0xff0000)
              await ctx.bot.say(embed=embed)
      

def setup(bot):
    bot.add_cog(botsorgapi)
