import json
import aiohttp
import asyncio
import os
import requests
import discord
from discord.ext import commands

with open("token_file2.pk1", "r") as token_file2:
  dbl = json.load(token_file2)
with open("token_file3.pk1", "r") as token_file3:
  bfd = json.load(token_file3)
bot=commands.Bot(command_prefix='s.')
ownerids=['221381001476046849', '221263215496134656']

url = "https://discordbots.org/api/bots/" + '375370278810681344' + "/stats"
headers = {"Authorization" : dbl}
uri = 'https://botsfordiscord.com/api/v1'


class botsorgapi():
  print('DBL API Loaded')
  
            
  @bot.command(pass_context = True, hidden = True)
  async def bfdLoad(ctx):
    if ctx.message.author.id not in ownerids:
      pass
    else:
        dump = json.dumps({'server_count': len(ctx.bot.servers)})
        head = {'authorization': bfd, 'content-type' : 'application/json'}

        url2 = '{0}/bots/375370278810681344'.format(uri)

        requests.post(url2, data=dump, headers=head)
        await ctx.bot.say("<:tickYes:315009125694177281> Succes!")
        
  
  @bot.command(pass_context = True, hidden = True)
  async def dblLoad(ctx):
    if ctx.message.author.id not in ownerids:
      pass
    else:
      try:
        payload = {"server_count"  : len(ctx.bot.servers)}
        requests.post(url, data=payload, headers=headers)
        await ctx.bot.say("<:tickYes:315009125694177281> Succes!")
      except Exception as e:
              embed = discord.Embed(title=":warning: Error!", description="Failed loading {0}\n{1}: {2}".format(extension, type(e).__name__, e), color=0xff0000)
              await ctx.bot.say(embed=embed)
      

def setup(bot):
    bot.add_cog(botsorgapi)
