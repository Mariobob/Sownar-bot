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

class Fun():
    print('Fun loaded')
    print('------')

    @bot.command(pass_context = True)
    async def fun(ctx):
        await ctx.bot.say("I am working!")
      
    @bot.command(pass_context = True)
    async def flip(ctx):
      flip = random.choice["Heads", "Tails"]
      await ctx.bot.say("It's {}!".format(flip))
    
    @bot.command(pass_context = True)
    async def roll(ctx):
      roll = random.choice["1", "2", "3", "4", "5", "6"]
      await ctx.bot.say("It's a {}!".format(roll))
      
    @bot.command(pass_context = True)
    async def rps(ctx, rps = str):
      if rps == "":
        await ctx.bot.say("Please specify [rock, paper or scissors]")
      else:
        rps_bot = random.choice["Rock", "Paper", "Scissors"]
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
          

def setup(bot):
    bot.add_cog(Fun)
