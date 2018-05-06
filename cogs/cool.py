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
from pyfiglet import figlet_format as ascii_format
  
def get_prefix(bot, message):
    if not os.path.isfile("prefixes_list.pk1"):
        prefix_list = []
    else:
        with open("prefixes_list.pk1", "r") as prefixs_list:
                prefix_list = json.load(prefixs_list)    
    prefixes = "s."
    if len(prefix_list) >= 1:

            for pre in prefix_list:
                    sid,spre = pre.split(":")
                    if sid == message.server.id:
                            prefixes = spre
            

    return prefixes

bot=commands.Bot(command_prefix=get_prefix)

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
    async def giveaway(ctx, duration=None, winners=None, *, prize=None):
      try:
        if duration is None:
          error = discord.Embed(title=":warning: Error!",description="`time` is a required input",color=0xff0000)
          await ctx.bot.say(embed=error)
        else:
          if winners is None:
            winners = 1
          if prize is None:
            error = discord.Embed(title=":warning: Error!",description="`prize` is a required input",color=0xff0000)
            await ctx.bot.say(embed=error)
          else:
            unit = duration[-1]
            if unit == 's':
              time = int(duration[:-1])
              longunit = 'seconds'
            elif unit == 'm':
              time = int(duration[:-1]) * 60
              longunit = 'minutes'
            elif unit == 'h':
              time = int(duration[:-1]) * 60 * 60
              longunit = 'hours'
            elif unit == 'd':
              time = int(duration[:-1]) * 60 * 60 * 24
              longunit = 'days'
            else:
              await ctx.bot.say('Invalid Unit! Use `s`, `m`, or `h`.')
            
            winners = int(winners)
            ga_users=[]
            ga=discord.Embed(title=":tada: NEW GIVEAWAY :tada:", description="-")
            ga.add_field(name=prize, value="Ends in **{0}** {1}".format(time, longunit), inline =False)
            ga.set_footer(text="{} winner".format(winners))
            ga_react = await ctx.bot.say(embed=ga)
            await ctx.bot.add_reaction(ga_react, "🎉")
            await asyncio.sleep(time)
            ga_message_id = ga_react.id
            ga_channel = ga_react.channel
            ga_message = await ctx.bot.get_message(ga_channel, ga_message_id)
            for user in await ctx.bot.get_reaction_users(ga_message.reactions[0]):
              ga_users.append(user.mention)
            sownar = ctx.message.server.get_member("375370278810681344")
            ga_users.remove(sownar.mention)
            if len(ga_users) < winners:
              error = discord.Embed(title=":warning: Error!",description="The giveaway ended with not enough participants, could not chose a winner",color=0xff0000)
              await ctx.bot.say(embed=error)
            else:
              winner_list = []
              for loop in range(winners):
                winner = random.choice(ga_users)
                ga_users.remove(winner)
                winner_list.append(winner)
              ga_end = discord.Embed(title=":tada: GIVEAWAY ENDED :tada:", description="-")
              ga_end.add_field(name="Winner(s)", value="\n".join(winner_list))
              await ctx.bot.edit_message(ga_react, embed = ga_end)
              await ctx.bot.say("Congrats {0}! You won **{1}**".format(", ".join(winner_list), prize))
      except ValueError:
        error = discord.Embed(title=":warning: Error!",description="Please use a number inputs for `time` and `winner`",color=0xff0000)
        await ctx.bot.say(embed=error)
      
      
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
      
    @bot.command(pass_context = True)
    async def created(ctx):
      date = ctx.message.server.created_at.strftime("%A, %b %d, %Y")
      await ctx.bot.say(date)
    
    @bot.command(pass_context = True, no_pm = True)  
    async def ascii(ctx, *, variable=None):
        if variable is None:
            embed = discord.Embed(title=':warning: Error', description='You need to write the argument!', color=0xff0000)
            await ctx.bot.say(embed=embed)
        else:
            await ctx.bot.say('```{}```'.format(ascii_format(variable)))
    
    @bot.command(pass_context = True, no_pm = True)
    async def urban(ctx, *,msg: str):
      word = ' '.join(msg)
      api = "http://api.urbandictionary.com/v0/define"
      response = requests.get(api, params=[("term", word)]).json()
        
    
      if len(response["list"]) == 0: 
        await ctx.bot.say("Could not find that word!")
        return
      
      embed = discord.Embed(title = ":mag: Word Searched:", description = msg, timestamp = datetime.datetime.utcnow())
      embed.add_field(name = "Top definition:", value = textwrap.shorten(response['list'][0]['definition'], width = 1024, placeholder = "..."))
      embed.add_field(name = "Examples:", value = response['list'][0]["example"])
      embed.set_footer(text = "Tags: " + ', '.join(response['tags']))
      try:
        await ctx.bot.say(embed = embed)
      except:
        await ctx.bot.say("Response too long! I am currently working on a fix for this")
      
def setup(bot):
    bot.add_cog(Cool)
