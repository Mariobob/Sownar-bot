import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback


prefix='s.'
bot=commands.Bot(command_prefix=prefix)
perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)
ownerids=['221381001476046849', '221263215496134656']
todo_list = []
finished_list = []

class Owner():
    print('Owner loaded')
    print('------')
    global owner
    owner = 1

    @bot.command(pass_context = True)
    async def own(ctx):
        await ctx.bot.say("I am working!")

    @bot.group(pass_context = True)
    async def todo(ctx):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if ctx.invoked_subcommand is None:
          
          if len(todo_list) == 0:
            await ctx.bot.say("Todo list is empty! Use `s.todo add [arg]`")
          else:
            num=0
            todo = discord.Embed(title="This stuff is todo !",description="Ranked from oldest to newest",color=0xff0000)
            for x in todo_list:
              num += 1
              todo.add_field(name=num, value=x, inline=False)
            await ctx.bot.say(embed=todo)
          
    @todo.command(pass_context = True)
    async def delete(ctx, *, item = None):
      if ctx.message.author.id not in ownerids:
        
        await ctx.bot.say(embed=perm_error)
      
      else:
        if item is None:
          await ctx.bot.say("Please specify an element")
        else:
          try:
            item = int(item)
          
            del todo_list[item-1]
            await ctx.bot.say("Successfully deleted element, **{}** from the list".format(item))
          except:
            await ctx.bot.say("You can only use numbers!")
            
    @todo.command(pass_context = True)
    async def add(ctx, *, todo: str):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if todo in todo_list:
          await ctx.bot.say("**{}** is already in the todo list".format(todo))
        else:
          todo_list.append(todo)
          await ctx.bot.say("Added **{}** to todo list".format(todo))
          
    @todo.command(pass_context=True)
    async def help(ctx):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        todohelp = discord.Embed(title='Todo command help', description="")
        todohelp.add_field(name="s.todo **help**", value= "show's this message", inline = False)
        todohelp.add_field(name="s.todo **add**", value= "add an element to the todo list", inline = False)
        todohelp.add_field(name="s.todo **delete**", value= "remove and element to the todo list", inline = False)
        await ctx.bot.say(embed=todohelp)
        
    @todo.command(pass_context = True)
    async def finish(ctx, *, item = None):
      if ctx.message.author.id not in ownerids:
        
        await ctx.bot.say(embed=perm_error)
      
      else:
        if item is None:
          await ctx.bot.say("Please specify an element")
        else:
          try:
            item = int(item)
            finished_list.append(todo_list[item-1])
            del todo_list[item-1]
            await ctx.bot.say("Successfully moved element, **{}** to the finished list".format(item))
          except:
            await ctx.bot.say("You can only use numbers!")
          


          
    @bot.command(pass_context = True)
    async def gameset(ctx, *, game = None):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        if game is None:
          embed = discord.Embed(title=":warning: Error!",description="Please specify a game status!",color=0xff0000)
          await ctx.bot.say(embed=embed)
        else:
          await ctx.bot.change_presence(game=discord.Game(name=game))
      
        

          
        

def setup(bot):
    bot.add_cog(Owner)
