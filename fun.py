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

flips = ["Heads", "Tails"]
rolls = ["1", "2", "3", "4", "5", "6"]
rpss = ["Rock", "Paper", "Scissors"]

class Fun():
    print('Fun loaded')
    print('------')

    @bot.command(pass_context = True)
    async def fun(ctx):
        await ctx.bot.say("I am working!")
      
    @bot.command(pass_context = True)
    async def flip(ctx):
      flip = random.choice(flips)
      embed = discord.Embed(title="Flipped...", description="It's {}".format(flip), color=0x00ff00)
      await ctx.bot.say(embed=embed)
      
    
    @bot.command(pass_context = True)
    async def roll(ctx):
      roll = random.choice(rolls)
      embed = discord.Embed(title="Rolled...", description="It's a {}".format(roll), color=0x00ff00)
      await ctx.bot.say(embed=embed)
      
      
    @bot.command(pass_context = True)
    async def rps(ctx):
      umsg = ctx.message.content.lower()
      args = umsg.split(' ')
      args = umsg.replace(args[0], "")
      args = args[1:]
      var = int(random.random() * 3)
      if args == "paper" or args == "rock" or args == "scissors":
        if (var == 0):
          if args == "paper":
            await ctx.bot.say("Rock, You win!")
          elif args == "rock":
            await ctx.bot.say("Rock, It's a draw!")
          elif args == "scissors":
            await ctx.bot.say("Rock, You lose!")
        elif (var == 1):
          if args == "paper":
            await ctx.bot.say("Paper, It's a draw!")
          elif args == "rock":
            await ctx.bot.say("Paper, You lose!")
          elif args == "scissors":
            await ctx.bot.say("Paper, You win!")
          elif (var == 2):
            if args == "paper":
              await ctx.bot.say("Scissors, You lose!")
            elif args == "rock":
              await ctx.bot.say("Scissors, You win!")
            elif args == "scissors":
              await ctx.bot.say("Scissors, It's a draw!")
      else:
          await ctx.bot.say(":x: You must specify either rock, paper, or scissors!")
          

def setup(bot):
    bot.add_cog(Fun)
