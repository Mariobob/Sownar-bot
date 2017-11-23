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
      await ctx.bot.say("It's {}!".format(flip))
    
    @bot.command(pass_context = True)
    async def roll(ctx):
      roll = random.choice(rolls)
      await ctx.bot.say("It's a {}!".format(roll))
      
    @bot.command(pass_context = True)
    async def rps(ctx, *, rps = str):
      if rps == "":
        await ctx.bot.say("Please specify [rock, paper or scissors]")
      else:
        rps_bot = random.choice(rpss)
        if rps == "rock":
          if rps_bot == "Paper":
            await ctx.bot.say("Paper! I win")
          elif rps_bot == "Scissors":
            await ctx.bot.say("Scissors! You win")
          elif rps_bot == "Rock":
            await ctx.bot.say("Rock! It's a tie")
        elif rps == "paper":
          if rps_bot == "Rock":
            await ctx.bot.say("Rock! You win")
          elif rps_bot == "Scissors":
            await ctx.bot.say("Scissors! I win")
          elif rps_bot == "Paper":
            await ctx.bot.say("Paper! It's a tie")
        elif rps == "scissors":
          if rps_bot == "Rock":
            await ctx.bot.say("Rock! I win")
          elif rps_bot == "Paper":
            await ctx.bot.say("Paper! You win")
          elif rps_bot == "Scissors":
            await ctx.bot.say("Scissors! It's a tie")
      await ctx.bot.say("Hmm, it seems like the command didn't function correctly. Please send my dev team a ticket `s.ticket [message]`")
      
    @bot.command(pass_context = True)
    async def rpsgod(ctx):
      umsg = ctx.message.content.lower()
      args = umsg.split(' ')
      args = umsg.replace(args[0], "")
      args = args[1:]
      var = int(random.random() * 3)
      if args == "paper" or args == "rock" or args == "scissors":
        if (var == 0):
          if args == "paper":
            await ctx.bot.say(":moyai: You win!")
          elif args == "rock":
            await ctx.bot.say(":moyai: It's a draw!")
          elif args == "scissors":
            await ctx.bot.say(":moyai: You lose!")
        elif (var == 1):
          if args == "paper":
            await ctx.bot.say(":newspaper: It's a draw!")
          elif args == "rock":
            await ctx.bot.say(":newspaper: You lose!")
          elif args == "scissors":
            await ctx.bot.say(":newspaper: You win!")
          elif (var == 2):
            if args == "paper":
              await ctx.bot.say(":scissors: You lose!")
            elif args == "rock":
              await ctx.bot.say(":scissors: You win!")
            elif args == "scissors":
              await ctx.bot.say(":scissors: It's a draw!")
      else:
          await ctx.bot.say(":x: You must specify either rock, paper, or scissors!")
          

def setup(bot):
    bot.add_cog(Fun)
