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
perm_errorbis = discord.Embed(title=":warning: Error!",description="I do not have the permission to use this command",color=0xff0000)

class Mod():
    print('Mod loaded')
    print('------')

    @bot.command(pass_context = True)
    async def mod(ctx):
        await ctx.bot.say("I am working!")

    @bot.command(pass_context = True)
    async def ban(ctx, *, member: discord.Member = None):
        if member is None:
          embed = discord.Embed(title=":warning: Error!",description="Who do I ban?",color=0xff0000)
          await ctx.bot.say(embed=embed)
    
        elif ctx.message.server.me.server_permissions.ban_members == True:
                if ctx.message.author.server_permissions.ban_members == True:
                    if ctx.message.author.top_role.position > member.top_role.position:
                        await ctx.bot.ban(member)
                        await ctx.bot.say(":white_check_mark: Succesfully banned {}".format(member))
                    else:
                        await ctx.bot.say(embed=perm_error)
                else:
                    await ctx.bot.say(embed=perm_error)
        else:
            await ctx.bot.say(embed=perm_errorbis)
            
    @bot.command(pass_context = True)
    async def kick(ctx, *, member: discord.Member = None):
        if member is None:
          embed = discord.Embed(title=":warning: Error!",description="Who do I kick?",color=0xff0000)
          await ctx.bot.say(embed=embed)
    
        if ctx.message.server.me.server_permissions.kick_members == True:
                if ctx.message.author.server_permissions.kick_members == True:
                    if ctx.message.author.top_role.position > member.top_role.position:
                        await ctx.bot.kick(member)
                        await ctx.bot.say(":white_check_mark: Succesfully kicked {}".format(member))
                    else:
                        await ctx.bot.say(embed=perm_error)
                else:
                    await ctx.bot.say(embed=perm_error)
        else:
            await ctx.bot.say(embed=perm_errorbis)
    
    @bot.command(pass_context = True)
    async def clear(ctx, number = None):
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
        await ctx.bot.purge_from(ctx.message.channel, limit=val)
    
    @bot.command(pass_context = True)
    async def prune(ctx, *, num = None):
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

def setup(bot):
    bot.add_cog(Mod)
