import discord
import asyncio
import json
import os
import datetime
from discord.ext import commands
import time
import traceback


logs = discord.Object("376778387676594176")
console = discord.Object("376552211817299968")
tickets = discord.Object("376563001643499522")
seconds=0
minutes=0
hours=0
days=0
weeks=0
prefix='s.'
ownerids=['221381001476046849', '221263215496134656']
todo_list=[]

perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)

class Main():
    print('main Loaded')
    print('------')
    

# -- Random.py --
#@ctx.bot.command(pass_context = True)
#async def say(ctx, *, echo: str):
#    await ctx.bot.say(echo)
    

    @commands.command(pass_context = True)
    async def todoadd(ctx, *, todo: str):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if todo in todo_list:
          await ctx.bot.say("**{}** is already in the todo list".format(todo))
        else:
          todo_list.append(todo)
          await ctx.bot.say("Added to todo list")

    @commands.command(pass_context = True)
    async def todo(ctx):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        num=0
        for x in todo_list:
          num += 1
          await ctx.bot.say("{0}: {1}".format(num, x))

    @commands.command(pass_context = True)
    async def tododel(ctx, *, item: int):
      if ctx.message.author.id not in ownerids:
        
        await ctx.bot.say(embed=perm_error)
      
      else:
        if item in todo_list:
          del todo_list[item]
          await ctx.bot.say("Successfully deleted **{}** from the list".format(item))
        else:
          await ctx.bot.say("Please use a valid todo item, s.todo")
        
def setup(bot):
    bot.add_cog(Main)


