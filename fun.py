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
slot = [":watermelon:", ":cherries:", ":lemon:", ":apple:", ":strawberry:", ":kiwi:"]

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
        casinohelp = discord.Embed(title="All casino commands", description= "`s.casino war`\n`s.casino slots`", color = 0xff0000)
        await ctx.bot.say(embed=casinohelp)
        
      
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
        
      war = discord.Embed(title = "**---Cards---**", description = "`Player: {}` \n`Computer: {}`".format(player, ai), color=dcolor)
      war.set_author(name="War", icon_url="http://www.clipartlord.com/wp-content/uploads/2014/08/playing-card5.png")
      war.add_field(name = "You {0}".format(winner), value="-", inline = False)
      war.set_footer(icon_url= ctx.message.author.avatar_url, text= "Requested by {}".format(ctx.message.author.name))
      await ctx.bot.say(embed=war)
      
    @casino.command(pass_context=True)
    async def slots(ctx):
      x=random.choice(slot)
      y=random.choice(slot)
      z=random.choice(slot)
      if x==y:
        if x==z:
          winner= "won, `3/3`"
          dcolor = 0x00ff00
        else:
          winner= "close, `2/3`"
          dcolor = 0xffae00
      elif y==z:
        winner= "close, `2/3`"
        dcolor = 0xffae00
      elif x==z:
        winner= "close, `2/3`"
        dcolor = 0xffae00
      else:
        winner= "lost, `0/3`"
        dcolor = 0xff0000
      
      slots = discord.Embed(title = "---Slots---", description = "{0}|{1}|{2}".format(x, y, z), color = dcolor)
      slots.set_author(name="Slots", icon_url="https://images.emojiterra.com/twitter/512px/1f3b0.png")
      slots.add_field(name= "You {}".format(winner), value="-", inline = False)
      slots.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author.name))
      await ctx.bot.say(embed=slots)
       
    @casino.command(pass_context=True, aliases=["21", "bj"])
    async def blackjack(ctx):
      bj_continue = 1
      player=randint(1,13)
      dealer=randint(1,13)
      dealshow="N/A"
      done = "false"
      humanplayer=ctx.message.author
      
      def bj_embed():
        if done == "false":
          bj = discord.Embed(title="---Hand---", description="`Player: {0}`\n`Dealer: {1}`".format(player, dealshow))
          bj.set_author(name="BlackJack", icon_url="http://www.emoji.co.uk/files/twitter-emojis/symbols-twitter/11272-playing-card-black-joker.png")
          bj.add_field(name="`Stand or Hit`?", value="Please react with :x: to take no more cards\nPlease type :white_check_mark: to take more cards", inline = False)
          bj.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
          return bj
        elif done == "true":
          bj = discord.Embed(title="---Hand---", description="`Player: {0}`\n`Dealer: {1}`".format(player, dealshow))
          bj.set_author(name="BlackJack", icon_url="http://www.emoji.co.uk/files/twitter-emojis/symbols-twitter/11272-playing-card-black-joker.png")
          bj.add_field(name="You {}".format(winorlose), value = "-", inline = False)
          bj.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
          return bj
      
      while bj_continue == 1:
        bj_message = await ctx.bot.send_message(ctx.message.channel, embed=bj_embed())
        await ctx.bot.add_reaction(bj_message, "✅")
        await ctx.bot.add_reaction(bj_message, "❌")
        res = await ctx.bot.wait_for_reaction(["✅", "❌"], message=bj_message)
        await ctx.bot.say("{0.user} reacted with {0.reaction.emoji}".format(res))
        
      
      
      
      
      
def setup(bot):
    bot.add_cog(Fun)
