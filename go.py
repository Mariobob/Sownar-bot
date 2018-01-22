import discord
import asyncio
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import aiohttp
import random

logs = discord.Object("376778387676594176")
console = discord.Object("376552211817299968")
tickets = discord.Object("376563001643499522")
status = discord.Object("404796496995942401")
seconds=0
minutes=0
hours=0
days=0
weeks=0
prefix=["s."]
ownerids=['221381001476046849', '221263215496134656']
with open("token_file.pk1", "r") as token_file:
  bottoken = json.load(token_file)
with open("token_file2.pk1", "r") as token_file2:
  dbl = json.load(token_file2)
global owner
owner = 0
global mod
mod = 0
global fun
fun = 0
global cool
cool = 0
global utils
utils = 0

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
bot.remove_command("help")
game = ('{0}help | {1} servers'.format(prefix, len(bot.servers)))
startup_extensions = ["utils", "mod", "fun", "owner", "cool", "modmail", "errorhandler", "dblAPI"]
perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)

async def get_uptime():
    await bot.wait_until_ready()
    global seconds
    seconds = 0
    global minutes
    minutes = 0
    global hours
    hours = 0
    global days
    days = 0
    global weeks
    weeks = 0
    while not bot.is_closed:
        await asyncio.sleep(1)
        seconds += 1
        if seconds==60:
            minutes += 1
            seconds = 0
        if minutes==60:
            hours += 1
            minutes = 0
        if hours==24:
            days += 1
            hours = 0
        if days==7:
            weeks += 1
            days = 0

      
async def game():
  await bot.wait_until_ready()
  while not bot.is_closed:
    await bot.change_presence(game=discord.Game(name='{0}help | {1} servers'.format(random.choice(prefix), len(bot.servers))))
    await asyncio.sleep(120)
    await bot.change_presence(game=discord.Game(name='{0}invite | {1} servers'.format(random.choice(prefix), len(bot.servers))))
    await asyncio.sleep(120)
    
class startup():
  
  @bot.event
  async def on_server_join(server):
    embed = discord.Embed(title="__Server Joined! {}__".format(server.name), color=0x00ff00, timestamp = datetime.datetime.utcnow())
    embed.set_footer(text="Updated Server Count: {}".format(len(bot.servers)))
    embed.add_field(name="Server Owner", value=server.owner, inline=True)
    embed.add_field(name="Member Count", value="{0} members".format(server.member_count), inline=True)
    embed.add_field(name="Server Region", value=server.region, inline=True)
    await bot.send_message(console, embed=embed)
    await bot.send_message(logs, embed=embed)
#    await aiohttp.ClientSession().post('https://discordbots.org/api/bots/' + str(bot.user.id) + '/stats/', json={"server_count": len(bot.servers)}, headers={'Authorization': dbl})

  @bot.event
  async def on_server_remove(server):
    embed = discord.Embed(title="__Server Left! {}__".format(server.name), color=0xff0000, timestamp = datetime.datetime.utcnow())
    embed.add_field(name="Server Owner", value=server.owner, inline=True)
    embed.set_footer(text="Updated Server Count: {}".format(len(bot.servers)))
    embed.add_field(name="Member Count", value="{0} members".format(server.member_count), inline=True)
    embed.add_field(name="Server Region", value=server.region, inline=True)
    await bot.send_message(console, embed=embed)
    await bot.send_message(logs, embed=embed)
#    await aiohttp.ClientSession().post('https://discordbots.org/api/bots/' + str(bot.user.id) + '/stats/', json={"server_count": len(bot.servers)}, headers={'Authorization': dbl})

  
  @bot.event
  async def on_ready():
    t1 = time.perf_counter()
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    print("Servers: {}".format(len(bot.servers)))
    print("------")
    bot.load_extension("utils")
    bot.load_extension("fun")
    bot.load_extension("owner")
    bot.load_extension("cool")
    bot.load_extension("mod")
    bot.load_extension("modmail")
    bot.load_extension("errorhandler")
    bot.load_extension("dblAPI")
    t2 = time.perf_counter()
    await bot.send_message(status, ":white_check_mark: Bot running! `Took {}ms`".format(round(t2-t1)*1000))
  
  
  @bot.command()
  async def uptime():
    msg = "{0} weeks, {1} days, {2} hours, {3} minutes and {4} seconds".format(weeks, days, hours, minutes, seconds)
    embed = discord.Embed(title="__Bot Uptime__", description=msg, color=0x000000)
    await bot.say(embed=embed)

  @bot.command(pass_context = True)
  async def reload(ctx, extension: str):
      if ctx.message.author.id not in ownerids:
          await bot.say(embed=perm_error)
      else:
        if extension == "all":
          bot.unload_extension("mod")
          bot.unload_extension("utils")
          bot.unload_extension("owner")
          bot.unload_extension("cool")
          bot.unload_extension("fun")
          bot.unload_extension("modmail")
          bot.unload_extension("errorhandler")
          bot.unload_extension("dblAPI")
          for extension in startup_extensions:
            try:
              t1 = time.perf_counter()
              bot.load_extension(extension)
              embed = discord.Embed(title=":white_check_mark: Success!", description="Successfully reloaded `{}`".format(extension), color=0x00ff00)
              t2 = time.perf_counter()
              embed.set_footer(text="Took {}ms".format(round(t2-t1)*1000))
              await ctx.bot.say(embed=embed)
            except Exception as e:
              embed = discord.Embed(title=":warning: Error!", description="Failed loading {0}\n{1}: {2}".format(extension, type(e).__name__, e), color=0xff0000)
        else:
          if extension in startup_extensions:
            bot.unload_extension(extension)
            try:
              t1 = time.perf_counter()
              bot.load_extension(extension)
              embed = discord.Embed(title=":white_check_mark: Success!", description="Successfully reloaded `{}`".format(extension), color=0x00ff00)
              t2 = time.perf_counter()
              embed.set_footer(text="Took {}ms".format(round(t2-t1)*1000))
            except Exception as e:
              embed = discord.Embed(title=":warning: Error!", description="Failed loading {0}\n{1}: {2}".format(extension, type(e).__name__, e), color=0xff0000)
          else:
            embed = discord.Embed(title=":warning: Error!", description="`{}` is not a cog, use `s.cogslist` for a list of all cogs".format(extension), color=0xff0000)
          await bot.say(embed=embed)
        
  @bot.command(pass_context = True)
  async def load(ctx, extension: str):
      if ctx.message.author.id not in ownerids:
          await bot.say(embed=perm_error)
      else:
        if extension in startup_extensions:
          bot.load_extension(extension)
          await bot.say("Extension **{}** loaded".format(extension))
        else:
          await bot.say("Not a valid extension, see `s.cogslist` for options")
    
  @bot.command(pass_context = True)
  async def unload(ctx, extension: str):
      if ctx.message.author.id not in ownerids:
          await bot.say(embed=perm_error)
      else:
        if extension in startup_extensions:
          bot.unload_extension(extension)
          await bot.say("Extension **{}** unloaded".format(extension))
        else:
          await bot.say("Not a valid extension, see `s.cogslist` for options")
          
        
  @bot.command(pass_context = True)
  async def cogslist(ctx):
      if ctx.message.author.id not in ownerids:
          await bot.say(embed=perm_error)
      else:
        cogs = discord.Embed(title="__Current Cogs!__", description="", color=0x00ff00)
        for cog in startup_extensions:
          cogs.add_field(name=cog, value="-", inline=False)
        await bot.say(embed=cogs)
        
  @bot.command(pass_context = True)
  async def restart(ctx):
    if ctx.message.author.id not in ownerids:
        await bot.say(embed=perm_error)
    else:
      await bot.send_message(status, ":x: Restarting...")
      for cog in startup_extensions:
        bot.unload_extension(cog)
      os.system("open " + '~/runbot_mac.command')
      exit()

bot.loop.create_task(game())
bot.loop.create_task(get_uptime())
bot.run(bottoken)
