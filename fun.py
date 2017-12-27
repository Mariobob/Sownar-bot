import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
from random import randint

prefix='s.'
bot=commands.Bot(command_prefix=prefix)

flips = ["Heads", "Tails"]
rolls = ["1", "2", "3", "4", "5", "6"]
rpss = ["Rock", "Paper", "Scissors"]
cards = ["Ace" ,"2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
ballgud = ["Signs point to yes", "You may rely on it", "It is certain", "Without a doubt"] 
ballbad = ["Don't count on it", "Outlook not so good", "Very doubtful", "Don't count on it"]
ballok = ["Reply hazy, try again later", "Concentrate and ask again"]

class Fun():
    print('Fun loaded')
    print('------')
    global fun
    fun = 1

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
          embed = discord.Embed(title=":x: Error", description="You must specify either rock, paper, or scissors!", color=0xff0000)
          await ctx.bot.say(embed=embed)
          
    @bot.command(name="8ball", pass_context = True)
    async def _8ball(ctx):
      umsg = ctx.message.content
      omsg = umsg.split(' ')
      args = umsg.replace(omsg[0], "")
      args = args[1:]
      if args != "":
        balls = randint(0, 2)
        if (balls == 0):
          answer = random.choice(ballgud)
          dcolor = 0x00ff00
        elif (balls == 1):
          answer = random.choice(ballbad)
          dcolor = 0xff0000
        elif (balls == 2):
          answer = random.choice(ballok)
          dcolor = 0xffae00
        embed = discord.Embed(title="{} ?".format(args), description=answer, color=dcolor)
        await ctx.bot.say(embed=embed)
          
      else:
        embed = discord.Embed(title=":x: Error", description="You need to specify a question", color=0xff0000)
        await ctx.bot.say(embed=embed)
    
    @bot.group(pass_context = True)
    async def casino(ctx):
      if ctx.invoked_subcommand is None:
        casinohelp = discord.Embed(title="All casino commands")
      
    @casino.command(pass_context = True)
    async def war(ctx):
      player = randint(1,13)
      ai = randint(1,13)
      if player > ai:
        winner = "won"
      elif ai > player:
        winner = "lost"
      elif ai == player:
        winner = "tied"
      if player == 10:
        player = "Jack"
      elif player == 11:
        player = "Queen"
      elif player == 12:
        player = "King"
      elif player == 13:
        player = "Ace"
      if ai == 10:
        ai = "Jack"
      elif ai == 11:
        ai = "Queen"
      elif ai == 12:
        ai = "King"
      elif ai == 13:
        ai = "Ace"
      if winner == "won":
        dcolor = 0x00ff00
      elif winner == "lost":
        dcolor = 0xff0000
      elif winner == "tied":
        dcolor = 0xffae00
        
      war = discord.Embed(title = ":hearts: :spades: :diamonds: :clubs:", description = "-", color=dcolor)
      war.add_field(name = "**---{}---**".format(ctx.message.author.name), value="`Player: {}` \n`Computer: {}`".format(player, ai), inline = False)
      war.add_field(name = "You {0}, {1}".format(winner, ctx.message.author.name), value="-", inline = False)
      await ctx.bot.say(embed=war)
      
      
def setup(bot):
    bot.add_cog(Fun)
