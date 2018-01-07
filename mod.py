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
perm_error = discord.Embed(title=":warning: Error!",description="You do not have sufficient permissions to use this command",color=0xff0000)
perm_errorbis = discord.Embed(title=":warning: Error!",description="I do not have sufficient permissions to perform that action",color=0xff0000)

class Mod():
    print('Mod loaded')
    print('------')
    global mod
    mod = 1

    @bot.command(pass_context = True, no_pm = True)
    async def mod(ctx):
        await ctx.bot.say("I am working!")

    @bot.command(pass_context = True, no_pm = True)
    async def ban(ctx, *, member: discord.Member = None):
        if member is None:
          embed = discord.Embed(title=":warning: Error!",description="Who do I ban?",color=0xff0000)
          await ctx.bot.say(embed=embed)
    
        elif ctx.message.server.me.server_permissions.ban_members == True:
                if ctx.message.author.server_permissions.ban_members == True:
                    if ctx.message.author.top_role > member.top_role:
                        await ctx.bot.ban(member)
                        await ctx.bot.say(":white_check_mark: Succesfully banned {}".format(member))
                    else:
                        perm_error.add_field(name="Missing permissions:", value="`Ban_Members`")
                        await ctx.bot.say(embed=perm_error)
                else:
                    perm_error.add_field(name="Missing permissions:", value="`Ban_Members`")
                    await ctx.bot.say(embed=perm_error)
        else:
            perm_errorbis.add_field(name="Missing permissions:", value="`Ban_Members`")
            await ctx.bot.say(embed=perm_errorbis)
            
    @bot.command(pass_context = True, no_pm = True)
    async def kick(ctx, *, member: discord.Member = None):
        if member is None:
          embed = discord.Embed(title=":warning: Error!",description="Who do I kick?",color=0xff0000)
          await ctx.bot.say(embed=embed)
    
        elif ctx.message.server.me.server_permissions.kick_members == True:
                if ctx.message.author.server_permissions.kick_members == True:
                    if ctx.message.author.top_role > member.top_role:
                        await ctx.bot.kick(member)
                        await ctx.bot.say(":white_check_mark: Succesfully kicked {}".format(member))
                    else:
                        perm_error.add_field(name="Missing permissions:", value="`Kick_Members`")
                        await ctx.bot.say(embed=perm_error)
                else:
                    perm_error.add_field(name="Missing permissions:", value="`Kick_Members`")
                    await ctx.bot.say(embed=perm_error)
        else:
            perm_errorbis.add_field(name="Missing permissions:", value="`Kick_Members`")
            await ctx.bot.say(embed=perm_errorbis)
    
    @bot.command(pass_context = True, no_pm = True)
    async def clear(ctx, number = None):
      if ctx.message.server.me.server_permissions.manage_messages == True:
        if ctx.message.author.server_permissions.manage_messages == True:
          if number is None:
            embed = discord.Embed(title=":warning: Error!",description="Please specify a number!",color=0xff0000)
            await ctx.bot.say(embed=embed)
          try:
            val = int(number)
          except ValueError:
            embed = discord.Embed(title=":warning: Error!",description="You must use a number from `1-100`",color=0xff0000)
            await ctx.bot.say(embed=embed)
          if val > 100:
            embed = discord.Embed(title=":warning: Error!",description="Number must be under 100",color=0xff0000)
            await ctx.bot.say(embed=embed)
          else:
            try:
              await ctx.bot.purge_from(ctx.message.channel, limit=val)
            except:
              embed = discord.Embed(title=":warning: Error!",description="Can't delete messages more than 14 days old",color=0xff0000)
              await ctx.bot.say(embed=embed)
        else:
          perm_error.add_field(name="Missing permissions:", value="`Manage_Messages`")
          await ctx.bot.say(embed=perm_error)
      else:
        perm_errorbis.add_field(name="Missing permissions:", value="`Manage_Messages`")
        await ctx.bot.say(embed=perm_errorbis)
        
    
    @bot.command(pass_context = True, no_pm = True)
    async def purge(ctx, *, num = None):
      if ctx.message.server.me.server_permissions.kick_members == True:
        if ctx.message.author.server_permissions.kick_members == True:
      
          if num is None:
            embed = discord.Embed(title=":warning: Error!",description="Please specify a number of days of inactivity!",color=0xff0000)
            await ctx.bot.say(embed=embed)
          try:
            num = int(num)
          except ValueError:
            embed = discord.Embed(title=":warning: Error!",description="You must use a number",color=0xff0000)
            await ctx.bot.say(embed=embed)
          if num > 30:
            embed = discord.Embed(title=":warning: Error!",description="You must use a number under 30",color=0xff0000)
            await ctx.bot.say(embed=embed)
          else:
            server = ctx.message.author.server
            usertotal = server.member_count
            await ctx.bot.prune_members(ctx.message.server, days=num)
            newusertotal = server.member_count
            pruned = (usertotal - newusertotal)
            await ctx.bot.say("Kicked {} inactive users".format(pruned))
        else:
          perm_error.add_field(name="Missing permissions:", value="`Kick_Members`")
          await ctx.bot.say(embed=perm_error)
      else:
        perm_errorbis.add_field(name="Missing permissions:", value="`Kick_Members`")
        await ctx.bot.say(embed=perm_errorbis)   
        
def setup(bot):
    bot.add_cog(Mod)
