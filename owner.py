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

class Owner():
    print('Owner loaded')
    print('------')

    @bot.command(pass_context = True)
    async def own(ctx):
        await ctx.bot.say("I am working!")
        
    @bot.command(pass_context = True)
    async def todoadd(ctx, *, todo: str):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if todo in todo_list:
          await ctx.bot.say("**{}** is already in the todo list".format(todo))
        else:
          todo_list.append(todo)
          await ctx.bot.say("Added **{}** to todo list".format(todo))

    @bot.command(pass_context = True)
    async def todo(ctx):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if len(todo_list) == 0:
          await ctx.bot.say("Todo list is empty! Use `s.todoadd [arg]`")
        else:
          num=0
          for x in todo_list:
            num += 1
            await ctx.bot.say("{0}: {1}".format(num, x))

    @bot.command(pass_context = True)
    async def tododel(ctx, *, item: int):
      if ctx.message.author.id not in ownerids:
        
        await ctx.bot.say(embed=perm_error)
      
      else:
        
          del todo_list[item-1]
          await ctx.bot.say("Successfully deleted element, **{}** from the list".format(item))
          
    @bot.command(pass_context = True)
    async def gameset(ctx, *, game = str):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        if game == "":
          embed = discord.Embed(title=":warning: Error!",description="Please specify a game status!",color=0xff0000)
          await ctx.bot.say(embed=embed)
        else:
          await ctx.bot.change_presence(game=game)
        

          
        

def setup(bot):
    bot.add_cog(Owner)
