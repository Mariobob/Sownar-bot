import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback

prefix=["s.", "s>", "s/"]
bot=commands.Bot(command_prefix=prefix)
ownerids=['221381001476046849', '221263215496134656']
mm_error = discord.Embed(title=":warning: Error!",description="Please use this command in DM with the bot :wink:",color=0xff0000)
perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)
support="https://discord.gg/HcMhj3q"
bl_ids=[]

class ModMail():
    print('ModMail loaded')
    print('------')
  
    @bot.command(pass_context = True, aliases=["modmail", "mailmod", "mail"])
    async def mm(ctx, *, msg:str):
        
      if ctx.message.channel.is_private is True:
        chan_id = ctx.message.channel.id
        if chan_id not in bl_ids:
          create = 'true'
          server= ctx.bot.get_server("396469778430296068")
          for chanl in list(server.channels):
            if chanl.name == ctx.message.channel.id:
              create = 'false'
              chan = chanl
              
          if create == 'true':
            chan = await ctx.bot.create_channel(server, chan_id)
            
          embed= discord.Embed(title="ModMail with {}".format(ctx.message.author), description=msg)
          await ctx.bot.send_message(chan, embed=embed)
          await ctx.bot.say("Succesfully sent message!")
        else:
          mm_bl = discord.Embed(color=0xff0000)
          mm_bl.add_field(name=":warning: Error!", value="You have been blacklisted, please join the '({})[{}]' if you consider this to be wrong".format("Support Server", support), inline=False)
          await ctx.bot.say(embed=mm_bl)
      else:
        await ctx.bot.say(embed=mm_error)
    
    @bot.command(pass_context = True, no_pm = True)
    async def mma(ctx, *, msg:str):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        user = discord.Object(ctx.message.channel.name)
        mma = discord.Embed(title="A Dev answered your question: ({})".format(ctx.message.author.name), description=msg)
        await ctx.bot.say("Successfully sent message!")
        await ctx.bot.send_message(user, embed=mma)
        
    @bot.command(pass_context = True, np_pm= True)
    async def mmbl(ctx):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        if ctx.message.channel.name in bl_ids:
          bl_ids.remove(ctx.message.channel.name)
          await ctx.bot.say("Successfully removed from the ModMail blacklist")
        else:
          await ctx.bot.say("Successfully added to the ModMail blacklist")
          bl_ids.append(ctx.message.channel.name)
          
      



def setup(bot):
  bot.add_cog(ModMail)
