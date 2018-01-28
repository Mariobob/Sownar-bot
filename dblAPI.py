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
yup = discord.Object('376552211817299968')

def apiload():
  try:
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)
    succes = ':white_check_mark: Succes!'
  except Exception as e:
    succes = "Failed loading {0}\n{1}: {2}".format('API', type(e).__name__, e)
  return succes
    


url = "https://discordbots.org/api/bots/" + '375370278810681344' + "/stats"
headers = {"Authorization" : dbl}

class botsorgapi():
  print('DBL API Loaded')
  
  @bot.event
  async def on_ready():
    await bot.send_message(yup, apiload())
    
  @bot.event
  async def on_server_join(server):
    await bot.send_message(yup, apiload())
    
  @bot.event
  async def on_server_remove(server):
    await bot.send_message(yup, apiload())
    
    
  @bot.command(pass_context = True, hidden = True)
  async def dblAPIload(ctx):
    if ctx.message.author.id not in ownerids:
      pass
    else:
      await bot.say(apiload())
      

def setup(bot):
    bot.add_cog(botsorgapi)
