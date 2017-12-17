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
    async def poll(ctx, *, message:str):
      author = ctx.message.author
      embed = discord.Embed(color=author.color, timestamp=datetime.datetime.utcnow())
      embed.set_author(name="Poll", icon_url=author.avatar_url)
      embed.description = message
      embed.set_footer(text=author.name)
      await ctx.bot.say(embed=embed)
      await bot.add_reaction("👍")
      await bot.add_reaction("👎")
      
    
def setup(bot):
    bot.add_cog(Cool)
