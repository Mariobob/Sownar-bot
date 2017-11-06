import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import requests

prefix='s.'
bot=commands.Bot(command_prefix=prefix)

class Mod():
    print('Mod loaded')
    print('------')

    @bot.command(pass_context = True)
    async def mod(ctx):
        await ctx.bot.say("I am working!")

    @bot.command(pass_context = True)
    async def ban(ctx, *, member: discord.Member = None):
        if member is None:
            await bot.say(ctx.message.author + ": Who do I ban ?")
    
        elif ctx.message.server.me.server_permissions.ban_members == True:
                if ctx.message.author.server_permissions.ban_members == True:
                    if ctx.message.author.top_role.position > member.top_role.position:
                        await bot.ban(member)
                        await bot.say(":white_check_mark: Succesfully banned {}".format(member))
                    else:
                        await bot.say("You can not kick someone equal or higher than yourself")
                else:
                    await bot.say("You do not have the permissions to do so")
        else:
            await bot.say("I do not have the permissions to do so")
            
    @bot.command(pass_context = True)
    async def kick(ctx, *, member: discord.Member = None):
        if member is None:
            await bot.say(ctx.message.author + ": Who do I kick ?")
    
        if ctx.message.server.me.server_permissions.kick_members == True:
                if ctx.message.author.server_permissions.kick_members == True:
                    if ctx.message.author.top_role.position > member.top_role.position:
                        await bot.kick(member)
                        await bot.say(":white_check_mark: Succesfully kicked {}".format(member))
                    else:
                        await bot.say("You can not kick someone equal or higher than yourself")
                else:
                    await bot.say("You do not have the permissions to do so")
        else:
            await bot.say("I do not have the permissions to do so")
    
    

def setup(bot):
    bot.add_cog(Mod)
