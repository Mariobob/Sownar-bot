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
    async def giveaway(ctx, *, time:int):
      ga_users=[]
      ga=discord.Embed(title=":tada: NEW GIVEAWAY :tada:", description="-")
      ga.add_field(name="None", value="Ends in {} seconds".format(time), inline =False)
      ga.set_footer(text="None winners")
      ga_react = await ctx.bot.say(embed=ga)
      await ctx.bot.add_reaction(ga_react, "🎉")
      remain = time
      for loop in range(time):
        await asyncio.sleep(1)
        remain = remain - 1
        ga_edit=discord.Embed(title=":tada: NEW GIVEAWAY :tada:", description="-")
        ga_edit.add_field(name="None", value="Ends in {} seconds".format(remain), inline =False)
        ga_edit.set_footer(text="None winners")
        await ctx.bot.edit_message(ga_react, embed = ga_edit)
      for user in bot.get_reaction_users("\U0001f389"):
        ga_users.append(user)
      winner = random.choice(ga_users)
      ga_end = discord.Embed(title=":tada: GIVEAWAY ENDED :tada:", description="Winner is None")
      await ctx.bot.edit_message(ga_react, embed = ga_end)
      
    @bot.command(pass_context = True, no_pm = True, aliases = ["countdown"])
    async def cdown(ctx, time:int):
      c_time = time
      c_embed = discord.Embed(title= "Countdown from {}".format(time), description="{} seconds remaining".format(c_time))
      c_down = await ctx.bot.say(embed=c_embed)
      for loop in range(time):
        await asyncio.sleep(1)
        c_time -= 1
        c_remain = discord.Embed(title= "Countdown from {}".format(time), description="{} seconds remaining".format(c_time))
        await ctx.bot.edit_message(c_down, embed = c_remain)
      c_done = discord.Embed(title="Countdown from {} finished !".format(time), description="Time's up!")
      await ctx.bot.edit_message(c_down, embed= c_done)
      
def setup(bot):
    bot.add_cog(Cool)
