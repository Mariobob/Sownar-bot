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
    
    @bot.command(pass_context = True, no_pm = True)
    async def rand(ctx):
        await ctx.bot.say("I am working!")
        
    @bot.command(pass_context = True, no_pm = True)
    async def say(ctx, *, echo: str):
      await ctx.bot.say(echo)
    
    @bot.command(pass_context = True, no_pm = True)
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
    
    @bot.command(pass_context = True, no_pm = True)
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
                  
    @bot.command(pass_context = True, no_pm = True)
    async def embed(ctx, *, message = None ):
      if message is None:
        error = discord.Embed(title=":warning: Error!",description="Please specify a message to embed!",color=0xff0000)
        await ctx.bot.say(embed=error)
      else:
        embed = discord.Embed(title = "", description=message)
        await ctx.bot.say(embed=embed)
    
    @bot.command(pass_context = True, no_pm = True)
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
    
    @bot.command(pass_context = True, no_pm = True)
    async def servericon(ctx):
      avatar = discord.Embed(title="Server icon", description="[{0}]({1})".format("Image", ctx.message.server.icon_url))
      avatar.set_image(url=ctx.message.server.icon_url)
      await ctx.bot.say(embed=avatar)
      
    @bot.command(pass_context = True, no_pm = True, aliases=["ga"])
    async def giveaway(ctx, *, time = None, winners = None, title = None):
      ga_users=[]
      if time is None:
        error = discord.Embed(title=":warning: Error!",description="Please specify a time in seconds",color=0xff0000)
        await ctx.bot.say(embed=error)
      elif winners is None:
        winners = 1
      elif title is None:
        error = discord.Embed(title=":warning: Error!",description="Please specify the giveaway item",color=0xff0000)
        await ctx.bot.say(embed=error)
      try:
        time = int(time)
      except:
        error = discord.Embed(title=":warning: Error!",description="Please specify a time in seconds",color=0xff0000)
        await ctx.bot.say(embed=error)
      try:
        winners = int(winners)
      except:
        error = discord.Embed(title=":warning: Error!",description="Please specify a number of winners",color=0xff0000)
        await ctx.bot.say(embed=error)
      
      ga=discord.Embed(title=":tada: NEW GIVEAWAY :tada:", description="-")
      ga.add_field(name=title, value="Ends in {} seconds".format(time), inline =False)
      ga.set_footer(text="{} winners".format(winners))
      ga_react = await ctx.bot.say(embed=ga)
      await ctx.bot.add_reaction(ga_react, "🎉")
      await asyncio.sleep(time)
      ga_end = discord.Embed(title=":tada: GIVEAWAY ENDED :tada:", description="Winner is None")
      await ctx.bot.edit_message(ga_react, embed = ga_end)
      
    
    
def setup(bot):
    bot.add_cog(Cool)
