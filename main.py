
import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import requests

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
startup_extensions = ["utils.py", "mod.py", "fun.py", "owner.py", "random.py"]

@bot.event
async def on_server_join(server):
    embed = discord.Embed(title="__Server Joined!__", description="I have joined a new server !", color=0x00ff00)
    embed.add_field(name="Server Name", value=server.name, inline=True)
    embed.add_field(name="Server Owner", value=server.owner, inline=True)
    embed.add_field(name="Member Count", value="{0} members".format(server.member_count), inline=True)
    embed.add_field(name="Server Region", value=server.region, inline=True)
    await bot.send_message(console, embed=embed)
    print("New server joined !")
    embed = discord.Embed(title="__Thanks for inviting me!__", description="If you have any questions regarding my commands, please use {0}help".format(prefix), color=0x00ff00)
    await bot.send_message(server.default_channel, embed=embed)
    
@bot.event
async def on_server_remove(server):
    embed = discord.Embed(title="__Server Left!__", description="I have left a server !", color=0xff0000)
    embed.add_field(name="Server Name", value=server.name, inline=True)
    embed.add_field(name="Server Owner", value=server.owner, inline=True)
    embed.add_field(name="Member Count", value="{0} members".format(server.member_count), inline=True)
    embed.add_field(name="Server Region", value=server.region, inline=True)
    await bot.send_message(console, embed=embed)
    print("Server Left")

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name=game))
    bot.load_extension("utils")
    bot.load_extension("fun")
    

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

# -- Random.py --
@bot.command(pass_context = True)
async def say(ctx, *, echo: str):
    await bot.say(echo)


@bot.command()
async def uptime():
    msg = "{0} weeks, {1} days, {2} hours, {3} minutes and {4} seconds".format(weeks, days, hours, minutes, seconds)
    embed = discord.Embed(title="__Bot Uptime__", description=msg, color=0x000000)
    await bot.say(embed=embed)

@bot.command(pass_context = True)
async def reload(ctx, ext_name: str):
    if ctx.message.author.id not in ownerids:
        await bot.say("You do not have permission to execute this command")
    else:
        bot.unload_extension(ext_name)
        bot.load_extension(ext_name)
        await bot.say("Extension **{}** reloaded".format(ext_name))
    
@bot.command(pass_context = True)
async def extlist(ctx):
    if ctx.message.author.id not in ownerids:
        await bot.say("You don not have permission to execute this command")
    else:
        await bot.say(startup_extensions)

@bot.command(pass_context = True)
async def todoadd(ctx, *, todo: str):
    if ctx.message.author.id not in ownerids:
        await bot.say("You do not have permission to execute this command")
    else:
        if not os.path.isfile("todo_file.pk1"):
            todo_list = []
        else:
            with open("todo_file.pk1", "r") as todo_file:
                todo_list = json.load(todo_file)
        todo_list.append(todo)
        with open("todo_file.pk1", "w") as todo_file:
            json.dump(todo_list, todo_file)
        await bot.say("Added to todo list")

@bot.command(pass_context = True)
async def todo(ctx):
    if ctx.message.author.id not in ownerids:
        await bot.say("You do not have permission to execute this command")
    else:
        with open("todo_file.pk1", "r") as todo_file:
            todo_list = json.load(todo_file)
        for item in todo_list:
            await bot.say('`item`')

@bot.command(pass_context = True)
async def tododel(ctx, *, item: str):
    try:
        with open('todo_file.pk1', 'r') as todo_list:        
            todo = json.load(todo_list)
    
        for element in todo:
            if item in element:
                del element[item]
    
        with open('todo_file.pk1', 'w') as todo_list:
            todo = json.dump(todo, todo_list)
    except IndexError:
        await bot.say("Please use a valid todo item")

bot.loop.create_task(get_uptime())
token = open("token.txt", "r")
bot.run(token.read())

