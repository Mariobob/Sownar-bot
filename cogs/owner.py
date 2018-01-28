import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import io
import textwrap
from contextlib import redirect_stdout
import re

def get_prefix(bot, message):
    if not os.path.isfile("prefixes_list.pk1"):
        prefix_list = []
    else:
        with open("prefixes_list.pk1", "r") as prefixs_list:
                prefix_list = json.load(prefixs_list)    
    prefixes = "s."
    if len(prefix_list) >= 1:

            for pre in prefix_list:
                    sid,spre = pre.split(":")
                    if sid == message.server.id:
                            prefixes = spre
            

    return prefixes

bot=commands.Bot(command_prefix=get_prefix)
perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)
ownerids=['221381001476046849', '221263215496134656']
todo_list = []
finished_list = []

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

class Owner():
    print('Owner loaded')
    print('------')
    global owner
    owner = 1

    @bot.command(pass_context = True, no_pm = True)
    async def own(ctx):
        await ctx.bot.say("I am working!")

    @bot.group(pass_context = True, no_pm = True)
    async def todo(ctx):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if ctx.invoked_subcommand is None:
          
          if len(todo_list) == 0:
            await ctx.bot.say("Todo list is empty! Use `s.todo add [arg]`")
          else:
            num=0
            todo = discord.Embed(title="This stuff is todo !",description="Ranked from oldest to newest",color=0xff0000)
            for x in todo_list:
              num += 1
              todo.add_field(name=num, value=x, inline=False)
            await ctx.bot.say(embed=todo)
          
    @todo.command(pass_context = True, no_pm = True)
    async def delete(ctx, *, item = None):
      if ctx.message.author.id not in ownerids:
        
        await ctx.bot.say(embed=perm_error)
      
      else:
        if item is None:
          await ctx.bot.say("Please specify an element")
        else:
          try:
            item = int(item)
          
            del todo_list[item-1]
            await ctx.bot.say("Successfully deleted element, **{}** from the list".format(item))
          except:
            await ctx.bot.say("You can only use numbers!")
            
    @todo.command(pass_context = True, no_pm = True)
    async def add(ctx, *, todo: str):
      if ctx.message.author.id not in ownerids:
          await ctx.bot.say(embed=perm_error)
      else:
        if todo in todo_list:
          await ctx.bot.say("**{}** is already in the todo list".format(todo))
        else:
          todo_list.append(todo)
          await ctx.bot.say("Added **{}** to todo list".format(todo))
          
    @todo.command(pass_context=True)
    async def help(ctx):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        todohelp = discord.Embed(title='Todo command help', description="")
        todohelp.add_field(name="s.todo **help**", value= "show's this message", inline = False)
        todohelp.add_field(name="s.todo **add**", value= "add an element to the todo list", inline = False)
        todohelp.add_field(name="s.todo **delete**", value= "remove and element to the todo list", inline = False)
        await ctx.bot.say(embed=todohelp)
        
    @todo.command(pass_context = True, no_pm = True)
    async def finish(ctx, *, item = None):
      if ctx.message.author.id not in ownerids:
        
        await ctx.bot.say(embed=perm_error)
      
      else:
        if item is None:
          await ctx.bot.say("Please specify an element")
        else:
          try:
            item = int(item)
            finished_list.append(todo_list[item-1])
            del todo_list[item-1]
            await ctx.bot.say("Successfully moved element, **{}** to the finished list".format(item))
          except:
            await ctx.bot.say("You can only use numbers!")
          


          

          
#    @bot.command(pass_context = True, no_pm = True)
#    async def changelog(ctx):
#      todo = discord.Embed(title="__Todo Functions__", description= "-", color=0xffae00)
#      finish = discord.Embed(title="__Recent Updates__", description="-", color=0x00ff00)
#      num = 0
#      for x in todo_list:
#        if num < 5:
#          num += 1
#          todo.add_field(name="> {}".format(num), value=x, inline = False)
#      num = 0
#      for x in finished_list:
#        if num < 5:
#          num += 1
#          finish.add_field(name="> {}".format(num), value = x, inline = False)
      
#      await ctx.bot.say(embed=todo)
#      await ctx.bot.say(embed=finish)
        


    @bot.command(pass_context = True, hidden=True, name='eval')
    async def _eval(ctx, *, body: str):
      if ctx.message.author.id in ownerids:
        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'guild': ctx.message.server,
            'message': ctx.message,
        }

        env.update(globals())
  
        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.bot.say(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.bot.say(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.bot.say(f'```py\n{value}\n```')
            else:
                await ctx.bot.say(f'```py\n{value}{ret}\n```')  
      else:
        await ctx.bot.say(embed=perm_error)
    
    @bot.command(pass_context = True, aliases = ["gameset"], hidden=True)
    async def presence(ctx, type=None, *, game=None):
      '''Change the bot's presence'''
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      
      if type is None:
          await ctx.bot.say(f'Usage: .`s.presence [game/stream/watch/listen] [message]`')
      else:
          if type == 'stream':
              await ctx.bot.change_presence(game=discord.Game(name=game, type=1, url='https://www.twitch.tv/batshal'), status='online')
              await ctx.bot.say(f'Set presence to. `Streaming {game}`')
          elif type == 'game':
              await ctx.bot.change_presence(game=discord.Game(name=game))
              await ctx.bot.say(f'Set presence to `Playing {game}`')
          elif type == 'watch':
              await ctx.bot.change_presence(game=discord.Game(name=game, type=3), afk=True)
              await ctx.bot.say(f'Set presence to `Watching {game}`')
          elif type == 'listen':
              await ctx.bot.change_presence(game=discord.Game(name=game, type=2), afk=True)
              await ctx.bot.say(f'Set presence to `Listening to {game}`')
          elif type == 'clear':
              await ctx.bot.change_presence(game=None)
              await ctx.bot.say('Cleared Presence')
          else:
              await ctx.bot.say('Usage: `.presence [game/stream/watch/listen] [message]`') 
    
    @bot.command(pass_context = True)
    async def setprefix(ctx, prefix=None):
      if prefix is None:
        await ctx.bot.say(":x: `prefix` is a required argument")
      else:
        
        if ctx.message.author.server_permissions.administrator is True or ctx.message.author.id in ownerids:
          prefix_list=[]
          already = 'no'
          with open("prefixes_list.pk1", "r") as prefixs_list:
                  prefix_list = json.load(prefixs_list)
          if len(prefix_list) >= 1:
                  
                  for pre in prefix_list:
                      sid,spre = pre.split(":")
                      if sid == ctx.message.server.id:
                              already = 'yes'
                              prefix_list.remove(pre)
                      else:
                              pass
          prefix_list.append('{}:{}'.format(ctx.message.server.id, prefix))
          with open("prefixes_list.pk1", "w") as prefixs_list:
                  json.dump(prefix_list, prefixs_list)
          await ctx.bot.say('<:tickYes:315009125694177281> New prefix is `{}`'.format(prefix))
        else:
          await ctx.bot.say(embed=perm_error)
          
    @bot.command(pass_context = True)
    async def sio(ctx, *, serverl):
      if ctx.message.author.id not in ownerids:
        await ctx.bot.say(embed=perm_error)
      else:
        if serverl == 'list':
          msg = []
          for server in ctx.bot.servers:
            msg.append('Name: {}, ID: {}'.format(server.name, server.id))
          try:
            await ctx.bot.say('\n'.join(msg))
          except:
            for elem in msg:
              await ctx.bot.say(elem)
        else:
          server = ctx.bot.get_server(serverl)
          i = 0
          humanusers = 0
          botusers = 0
          online = 0
          voicechanneles = 0
          textchannels = 0 
          totalusers = 0
          totalchannels = 0
          totalroles = 0
          for members in server.members:
            totalusers += 1
            if members.bot is True:
              botusers += 1
            else:
              humanusers += 1
          for channels in server.channels:
            totalchannels += 1
          for roles in server.roles:
            totalroles += 1
          
        
          ago = (ctx.message.timestamp - server.created_at).days
          embed = discord.Embed(title= "Server", description="-", color=0x00ff00)
          embed.set_thumbnail(url=server.icon_url)
          embed.add_field(name="Server Name", value="Name: {0} \nID: {1}".format(server.name, server.id), inline=False)
          embed.add_field(name="Server Owner", value="Name: {0} \nID: {1}".format(server.owner, server.owner.id), inline=False)
          embed.add_field(name="Member Count", value="- {0} humans \n- {1} bots \n- {2} total".format(humanusers, botusers, totalusers), inline=False)
          embed.add_field(name="Channels", value="Total Channels : {0}".format(totalchannels), inline=False)
          embed.add_field(name="Roles", value=totalroles, inline=False)
          embed.add_field(name="Verification Level", value=server.verification_level, inline=False)
          embed.add_field(name="Server Region", value=server.region, inline=False)
          embed.add_field(name="Server created at", value="***{0}***, about {1} days ago".format(str(server.created_at.strftime("%A, %b %d, %Y")), ago), inline=False)
          await ctx.bot.say(embed=embed)
          
    @bot.command(pass_context = True)
    async def emoji(ctx, emoji, *, search=None):
          goodmoji = 'N/A'
          tot = []
          if ctx.message.author.id not in ownerids:
            await ctx.bot.say(embed=perm_error)
          else:
            if emoji == 'search':
              for moji in ctx.bot.get_all_emojis():
                match = re.search(search, moji.name)
                if match:
                  tot.append(moji.name)
                else:
                  pass
              if len(tot) == 0:
                await ctx.bot.say("No emoji's found")
              else:
                msg = '\n'.join(tot)
                await ctx.bot.say('```{}```'.format(msg))
            elif emoji == 'list':
              for moji in ctx.bot.get_all_emojis():
                tot.append(moji.name)
              try:
                await ctx.bot.say('\n'.join(tot))
              except:
                for elem in tot:
                  await ctx.bot.say(elem)
                  
              
            else:
              for moji in ctx.bot.get_all_emojis():
                if moji.name == emoji:
                  goodmoji = moji
              if goodmoji == 'N/A':
                await ctx.bot.say(':x: No emojis found')
              else:
                mojiemoji = "<:{0}:{1}>".format(goodmoji.name, goodmoji.id)
                em = discord.Embed(title = goodmoji.name, description = goodmoji.id)
                em.add_field(name='From server', value = goodmoji.server.name, inline = False)
                em.set_image(url=goodmoji.url)
                em.add_field(name='Emoji:', value= '`<:{0}:{1}>` - {2}'.format(goodmoji.name, goodmoji.id, mojiemoji))
                await ctx.bot.say(embed=em)
          
              
          
          
  

          
        

def setup(bot):
    bot.add_cog(Owner)
