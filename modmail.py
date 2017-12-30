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
ownerids=['221381001476046849', '221263215496134656']
mm_error = discord.Embed(title=":warning: Error!",description="Please use this command in DM with the bot :wink:",color=0xff0000)
perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)


class ModMail():
    print('ModMail loaded')
    print('------')
  
    @bot.command(pass_context = True, aliases=["modmail", "mailmod", "mail"])
    async def mm(ctx, *, msg:str):
      if ctx.message.channel.is_private is True:
        chan_id = ctx.message.channel.id
        server= ctx.bot.get_server("376096854448013325")
        everyone_perms = discord.PermissionOverwrite(read_messages=False)
        my_perms = discord.PermissionOverwrite(read_messages=True)
        everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
        mine = discord.ChannelPermissions(target=server.me, overwrite=my_perms)
        chan= await ctx.bot.create_channel(server, chan_id, everyone, mine)
        embed= discord.Embed(title="ModMail with {}".format(ctx.message.author), description=msg)
        await ctx.bot.send_message(chan, embed=embed)
      else:
        await ctx.bot.say(embed=mm_error)
    
    @bot.command(pass_context = True)
    async def mma(ctx, *, msg:str):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        user = discord.Object(ctx.message.channel.name)
        mma = discord.Embed(title="A Dev answered your question: {}".format(ctx.message.author.name), description=msg)
        await ctx.bot.send_message(user, embed=mma)
      



def setup(bot):
  bot.add_cog(ModMail)
