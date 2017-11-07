import discord
import asyncio
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
#import requests

console = discord.Object("376552211817299968")
tickets = discord.Object("376563001643499522")
seconds=0
minutes=0
hours=0
days=0
weeks=0
prefix='s.'
ownerids=['221381001476046849', '221263215496134656']

bot=commands.Bot(command_prefix=prefix)
bot.remove_command("help")
game = ('{0}help | {1} servers'.format(prefix, len(bot.servers)))
startup_extensions = ["utils", "mod", "fun", "owner", "random", "main"]
perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)

@bot.event()
async def on_ready():
  print("Logged in as")
  print(bot.user.name)
  print(bot.user.id)
  print("------")
  bot.load_extension("utils")
  bot.load_extension("fun")
  bot.load_extension("main")
  bot.load_extension("owner")
  bot.load_extension("random")
  bot.load_extension("mod")

@bot.event()
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

@bot.command()
async def uptime():
    msg = "{0} weeks, {1} days, {2} hours, {3} minutes and {4} seconds".format(weeks, days, hours, minutes, seconds)
    embed = discord.Embed(title="__Bot Uptime__", description=msg, color=0x000000)
    await bot.say(embed=embed)

@bot.command(pass_context = True)
async def reload(ctx, ext_name: str):
    if ctx.message.author.id not in ownerids:
        await bot.say(embed=perm_error)
    else:
      if ext_name in startup_extensions:
        bot.unload_extension(ext_name)
        bot.load_extension(ext_name)
        await bot.say("Extension **{}** reloaded".format(ext_name))
      else:
        await bot.say("Not a valid extension, see s.extlist for options")
        
@bot.command(pass_context = True)
async def load(ctx, ext_name: str):
    if ctx.message.author.id not in ownerids:
        await bot.say(embed=perm_error)
    else:
      if ext_name in startup_extensions:
        bot.load_extension(ext_name)
        await bot.say("Extension **{}** loaded".format(ext_name))
      else:
        await bot.say("Not a valid extension, see s.extlist for options")
    
@bot.command(pass_context = True)
async def unload(ctx, ext_name: str):
    if ctx.message.author.id not in ownerids:
        await bot.say(embed=perm_error)
    else:
      if ext_name in startup_extensions:
        bot.unload_extension(ext_name)
        await bot.say("Extension **{}** unloaded".format(ext_name))
      else:
        await bot.say("Not a valid extension, see s.extlist for options")
        
@bot.command(pass_context = True)
async def extlist(ctx):
    if ctx.message.author.id not in ownerids:
        await bot.say(embed=perm_error)
    else:
        for item in todo_list:
            await bot.say('`item`')


bot.loop.create_task(get_uptime())
token = open("token.txt", "r")
bot.run(token.read())
