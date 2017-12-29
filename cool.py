import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import aiohttp
import requests



prefix='s.'
bot=commands.Bot(command_prefix=prefix)

class Cool():
    print('random loaded')
    print('------')
    global cool
    cool = 1
    
    @bot.command(pass_context = True)
    async def rand(ctx):
        await ctx.bot.say("I am working!")
        
    @bot.command(pass_context = True)
    async def say(ctx, *, echo: str):
      await ctx.bot.say(echo)
    
    @bot.command(pass_context = True)
    async def cat(ctx):
      api = 'https://random.cat/meow'
      async with aiohttp.ClientSession() as session:
          async with session.get(api) as r:
              if r.status == 200:
                  response = await r.json()
                  embed = discord.Embed(title="Random Cat picture!", description="")
                  embed.set_image(url=response['file'])
                  await ctx.bot.say(embed=embed)
              else:
                  await ctx.bot.say('Error accessing the API')
    
    @bot.command(pass_context = True)
    async def dog(ctx):            
      api = "https://api.thedogapi.co.uk/v2/dog.php"
      async with aiohttp.ClientSession() as session:
          async with session.get(api) as r:
              if r.status == 200:
                  response = await r.json()
                  embed = discord.Embed(title="Random Dog picture!", description="")
                  embed.set_image(url=response['data'][0]["url"])
                  await ctx.bot.say(embed=embed)
              else:
                  x = "Could not find a dog :sad:!"
                  embed = discord.Embed(title='Error')
                  embed.description = x
                  await ctx.bot.say(embed=embed)
                  
    @bot.command(pass_context=True)
    async def embed(ctx, *, message = None ):
      if message is None:
        error = discord.Embed(title=":warning: Error!",description="Please specify a message to embed!",color=0xff0000)
        await ctx.bot.say(embed=error)
      else:
        embed = discord.Embed(title = "", description=message)
        await ctx.bot.say(embed=embed)
    
    @bot.command(pass_context=True)
    async def avatar(ctx, *, member: discord.Member = None):
      if member is None:
        user = ctx.message.author
      else:
        user = member
      avatars = user.avatar_url
      if ".gif" in avatars:
        avatars += "&f=.gif"
      avatar = discord.Embed(title="{}'s avatar".format(user.name), description="[{0}]({1})".format("Image", user.avatar_url))
      avatar.set_image(url=avatars)
      await ctx.bot.say(embed=avatar)
    
    @bot.command(pass_context=True)
    async def servericon(ctx):
      avatar = discord.Embed(title="Server icon", description="[{0}]({1})".format("Image", ctx.message.server.icon_url))
      avatar.set_image(url=ctx.message.server.icon_url)
      await ctx.bot.say(embed=avatar)
    
    @commands.command()
    async def urban(self, ctx, *,msg: str):
      word = ' '.join(msg)
      api = "http://api.urbandictionary.com/v0/define"
      response = requests.get(api, params=[("term", word)]).json()
    
     if len(response["list"]) == 0: return await ctx.bot.say("Could not find that word!")
     
      embed = discord.Embed(title = ":mag: Search Word", description = word, color = 0xffffff)
      embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
      embed.add_field(name = "Examples:", value = response['list'][0]["example"])
      embed.set_footer(text = "Tags: " + ', '.join(response['tags']))

      await ctx.bot.say(embed = embed)
        
    
    
def setup(bot):
    bot.add_cog(Cool)
