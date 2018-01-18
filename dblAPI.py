import json
import aiohttp
import asyncio
import os
import requests

with open("token_file2.pk1", "r") as token_file2:
  dbl = json.load(token_file2)
bot=commands.Bot(command_prefix='s.')

url = "https://discordbots.org/api/bots/" + '375370278810681344' + "/stats"
headers = {"Authorization" : dbl}

class botsorgapi():
  print('DBL API Loaded')
  
  @bot.event
  async def on_ready():
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)
    
  @bot.event
  async def on_server_join(server):
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)
    
  @bot.event
  async def on_server_remove(server):
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)

def setup(bot):
    bot.add_cog(botsorgapi)
