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
          if not os.path.isfile("todo_file.pk1"):
              todo_list = []
          else:
              with open("todo_file.pk1", "r") as todo_file:
                  todo_list = json.load(todo_file)
          todo_list.append(todo)
          with open("todo_file.pk1", "w") as todo_file:
              json.dump(todo_list, todo_file)
          await ctx.bot.say("Added to todo list")

    @commands.command(pass_context = True)
    async def todo(ctx):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
          with open("todo_file.pk1", "r") as todo_file:
              todo_list = json.load(todo_file)
          for item in todo_list:
              await ctx.bot.say(item)

    @commands.command(pass_context = True)
    async def tododel(ctx, *, item: str):
      if item == "":
        await ctx.bot.say("Please specify an argument")
      else:
        if ctx.message.author.id not in ownerids:
          
          await ctx.bot.say(embed=perm_error)
        else:
         try:
           with open('todo_file.pk1', 'r') as todo_list:
             todo = json.load(todo_list)
           for element in todo:
             if item in element:
               del element(item)
      
           with open('todo_file.pk1', 'w') as todo_list:
              todo = json.dump(todo, todo_list)
         except IndexError:
          await ctx.bot.say("Please use a valid todo item")
        
def setup(bot):
    bot.add_cog(Main)


