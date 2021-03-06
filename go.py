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
import requests

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
with open("token_file3.pk1", "r") as token_file3:
  bfd = json.load(token_file3)
with open("token_file4.pk1", "r") as token_file4:
  dbw = json.load(token_file4)
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
url = "https://discordbots.org/api/bots/" + '375370278810681344' + "/stats"
headers = {"Authorization" : dbl}
uri = 'https://botsfordiscord.com/api/v1'


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
startup_extensions = ["utils", "mod", "fun", "owner", "cool", "modmail", "errorhandler", "dblAPI", "image"]
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
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)
    print('DBL SERVER COUNT UPDATED')
    dump = json.dumps({'server_count': len(bot.servers)})
    head = {'authorization': bfd, 'content-type' : 'application/json'}
    url2 = '{0}/bots/375370278810681344'.format(uri)
    requests.post(url2, data=dump, headers=head)
    print('BFD SERVER COUNT UPDATED')
    payload = {"guild_count": len(bot.servers)}
    head = {'Authorization': dbw}
    url3 = 'https://discordbot.world/api/bot/' + bot.user.id + '/stats'
    requests.post(url3, data = payload, headers = head)
    print('DBW SERVER COUNT UPDATED')
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
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)
    print('DBL SERVER COUNT UPDATED')
    dump = json.dumps({'server_count': len(bot.servers)})
    head = {'authorization': bfd, 'content-type' : 'application/json'}
    url2 = '{0}/bots/375370278810681344'.format(uri)
    requests.post(url2, data=dump, headers=head)
    print('BFD SERVER COUNT UPDATED')
    payload = {"guild_count": len(bot.servers)}
    head = {'Authorization': dbw}
    url3 = 'https://discordbot.world/api/bot/' + bot.user.id + '/stats'
    requests.post(url3, data = payload, headers = head)
    print('DBW SERVER COUNT UPDATED')
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
    bot.load_extension("cogs.utils")
    bot.load_extension("cogs.fun")
    bot.load_extension("cogs.owner")
    bot.load_extension("cogs.cool")
    bot.load_extension("cogs.mod")
    bot.load_extension("cogs.modmail")
    bot.load_extension("cogs.errorhandler")
    bot.load_extension("cogs.dblAPI")
    bot.load_extension("cogs.image")
    payload = {"server_count"  : len(bot.servers)}
    requests.post(url, data=payload, headers=headers)
    print('DBL SERVER COUNT UPDATED')
    dump = json.dumps({'server_count': len(bot.servers)})
    head = {'authorization': bfd, 'content-type' : 'application/json'}
    url2 = '{0}/bots/375370278810681344'.format(uri)
    requests.post(url2, data=dump, headers=head)
    print('BFD SERVER COUNT UPDATED')
    payload = {"guild_count": len(bot.servers)}
    head = {'Authorization': dbw}
    url3 = 'https://discordbot.world/api/bot/' + str(bot.user.id) + '/stats'
    requests.post(url3, data = payload, headers = head)
    print('DBW SERVER COUNT UPDATED')
    t2 = time.perf_counter()
    await bot.send_message(status, ":white_check_mark: Bot running! `Took {}ms`".format('%.1f' % round((t2-t1)*1000), 1))
  
  @bot.event
  async def on_message(message):
      if message.author.bot:
          return
      await bot.process_commands(message)
      
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
          t1 = time.perf_counter()
          bot.unload_extension("cogs.mod")
          bot.unload_extension("cogs.utils")
          bot.unload_extension("cogs.owner")
          bot.unload_extension("cogs.cool")
          bot.unload_extension("cogs.fun")
          bot.unload_extension("cogs.modmail")
          bot.unload_extension("cogs.errorhandler")
          bot.unload_extension("cogs.dblAPI")
          bot.unload_extension("cogs.image")
          for extension in startup_extensions:
            try:
              bot.load_extension('cogs.{}'.format(extension))
              embed = discord.Embed(title=":white_check_mark: Success!", description="Successfully reloaded `{}`".format(extension), color=0x00ff00)
              t2 = time.perf_counter()
              embed.set_footer(text="Took {}ms".format('%.1f' % round((t2-t1)*1000), 1))
              await bot.say(embed=embed)
            except Exception as e:
              embed = discord.Embed(title=":warning: Error!", description="Failed loading {0}\n{1}: {2}".format(extension, type(e).__name__, e), color=0xff0000)
        else:
          if extension in startup_extensions:
            t1 = time.perf_counter()
            bot.unload_extension('cogs.{}'.format(extension))
            try:
              bot.load_extension('cogs.{}'.format(extension))
              embed = discord.Embed(title=":white_check_mark: Success!", description="Successfully reloaded `{}`".format(extension), color=0x00ff00)
              t2 = time.perf_counter()
              embed.set_footer(text="Took {}ms".format('%.1f' % round((t2-t1)*1000), 1))
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
          bot.load_extension('cogs.{}'.format(extension))
          await bot.say("Extension **{}** loaded".format(extension))
        else:
          await bot.say("Not a valid extension, see `s.cogslist` for options")
    
  @bot.command(pass_context = True)
  async def unload(ctx, extension: str):
      if ctx.message.author.id not in ownerids:
          await bot.say(embed=perm_error)
      else:
        if extension in startup_extensions:
          bot.unload_extension('cogs.{}'.format(extension))
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
