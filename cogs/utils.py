import discord
import asyncio
import random
import json
import os
import datetime
from discord.ext import commands
import time
import traceback
import unicodedata
import platform
import psutil

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
tickets = discord.Object("376563001643499522")
suggest = discord.Object('376776759221288961')
bot_invite="https://discordapp.com/oauth2/authorize?client_id=375370278810681344&scope=bot&permissions=2146958583"
support="https://discord.gg/HcMhj3q"
bot.remove_command('help')
beta_ids = ["200598766804271104", "382508564540948492", "221381001476046849"]

class Utils():
    print('Utils Loaded')
    print('------')
    global utils
    utils = 1
    

    @commands.command(pass_context = True, no_pm = True, aliases=["si", "server"])
    async def serverinfo(ctx):
        server = ctx.message.server
        i = 0
        humanusers = 0
        botusers = 0
        voicechanneles = 0
        textchannels = 0 
        totalusers = 0
        totalchannels = 0
        totalroles = 0
        online = 0
        idle = 0
        dnd = 0
        offline = 0
        bots = 0
        humans = 0
        total = 0
        for members in server.members:
          totalusers += 1
          if members.bot is True:
            botusers += 1
          else:
            humanusers += 1
          lm = str(members.status)
          if str(lm) == 'online':
            online += 1
          elif str(lm) == 'idle':
            idle += 1
          elif str(lm) == 'dnd':
            dnd += 1
          else:
            offline += 1
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
        embed.add_field(name="Member Statuses", value="<:online:313956277808005120> `{}`\n<:away:313956277220802560> `{}`\n<:dnd:313956276893646850> `{}`\n<:offline:313956277237710868> `{}`".format(online, idle, dnd, offline))
        embed.add_field(name="Channels", value="Total Channels : {0}".format(totalchannels), inline=False)
        embed.add_field(name="Roles", value=totalroles, inline=False)
        embed.add_field(name="Verification Level", value=server.verification_level, inline=False)
        embed.add_field(name="Server Region", value=server.region, inline=False)
        embed.add_field(name="Server created at", value="***{0}***, about {1} days ago".format(str(server.created_at.strftime("%A, %b %d, %Y")), ago), inline=False)
        await ctx.bot.say(embed=embed)

    @commands.command(pass_context = True, no_pm = True)
    async def test(ctx):
        await ctx.bot.say("I am working!")

    @commands.command(pass_context = True, no_pm = True, aliases=["ticket", "bug"])
    async def report(ctx, *, ticket: str):
        embed = discord.Embed(title="__New Ticket!__", description="I have recieved a new ticket !", color=0x00ff00)
        embed.add_field(name="Sent by", value=ctx.message.author, inline=True)
        embed.add_field(name="Ticket", value=ticket, inline=True)
        embed.set_footer(text="From: {}".format(ctx.message.server), icon_url=ctx.message.server.icon_url)
        await ctx.bot.delete_message(ctx.message)
        await ctx.bot.send_message(tickets, embed=embed)
        await ctx.bot.say("Your ticket has been sent to my dev team!")

    @commands.command(pass_context = True, no_pm = True)
    async def ping(ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await ctx.bot.send_typing(channel)
        t2 = time.perf_counter()
        await ctx.bot.say("Pong! `{}ms`".format(round((t2-t1)*1000)))

    @commands.command(pass_context = True, no_pm = True)
    async def invite(ctx):
      try:
        embed = discord.Embed(title=":link: __Bot Links__", description='[{}]({})''\n[{}]({})'.format("Bot invite", bot_invite, "Support Server", support), color=0x00ff00)
        await ctx.bot.send_message(ctx.message.author, embed=embed)
        await ctx.bot.send_message(ctx.message.channel, "Check your DM's :envelope_with_arrow:")
      except:
        todo = discord.Embed(title=":warning: Error!",description="An error occured, you may have DM's disabled",color=0xff0000)
        await ctx.bot.say(embed = todo)

    @commands.group(pass_context = True, no_pm = True)
    async def help(ctx):
      if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="__Bot commands!__", description="Total commands: {}".format(len(ctx.bot.commands)), color=0x00ff00)
        embed.add_field(name="Utility", value="`s.help utility`", inline=False)
        embed.add_field(name="Fun", value="`s.help fun`", inline=False)
        embed.add_field(name="Moderation", value="`s.help mod`", inline=False)
        embed.add_field(name="Misc", value="`s.help misc`", inline=False)
        embed.add_field(name="Image", value="`s.help image`", inline=False)
        embed.add_field(name="Support", value="`s.help support`", inline=False)
        if ctx.message.author.id not in beta_ids:
          await ctx.bot.say(embed=embed)
        else:
          embed.add_field(name="Beta Features", value="`s.help beta`", inline=False)
          await ctx.bot.say(embed=embed)
    
    @help.command(pass_context = True, no_pm = True)
    async def utility(ctx):
      util = discord.Embed(title="__Utility commands!__", description="-", color=0x00ff00)
      util.add_field(name="s.servers", value="Show the number of servers and members the bot is serving", inline=False)
      util.add_field(name="s.serverinfo", value="Shows information on the server", inline=False)
      util.add_field(name="s.perms [users]", value="Shows users permissions (if left empty author's permissions will be brought up)", inline=False)
      util.add_field(name="s.userinfo [user]", value="Shows information on the user (if left empty author's info will be brought up)", inline=False)
      util.add_field(name="s.id [user]", value="Get's a user's id (if left empty author's id will be brought up)", inline=False)
      util.add_field(name="~~s.info~~", value="Shows info on the bot", inline=False)
      util.add_field(name="s.ping", value="Shows the bot's latency", inline=False)
      util.add_field(name="s.uptime", value="Shows the bot's uptime", inline=False)
      util.add_field(name="s.setprefix [prefix]", value="Set's a new custom prefix for the server", inline=False)
      await ctx.bot.say(embed=util)
      
    @help.command(pass_context = True, no_pm = True)
    async def fun(ctx):
      fun = discord.Embed(title="__Fun commands!__", description="-", color=0x00ff00)
      fun.add_field(name="s.flip", value="Flips a coin", inline=False)
      fun.add_field(name="s.roll", value="Rolls a dice", inline=False)
      fun.add_field(name="s.8ball [question]", value="See's what the 8ball has to answer", inline=False)
      fun.add_field(name="s.rps [rock/paper/scissors]", value="Plays a game of rock, paper, scissors", inline=False)
      fun.add_field(name="s.slots", value="Roll the slots", inline=False)
      fun.add_field(name="s.war", value="Play a game of war (card game)", inline=False)
      fun.add_field(name="s.blackjack", value="Play a game of BlackJack", inline=False)
      await ctx.bot.say(embed=fun)
    
    @help.command(pass_context = True, no_pm = True)
    async def misc(ctx):
      cool = discord.Embed(title="__Misc commands!__", description="-", color=0x00ff00)
      cool.add_field(name="s.dog", value="Gets a dog picture", inline=False)
      cool.add_field(name="s.say [message]", value="Repeats your message", inline=False)
      cool.add_field(name="s.cat", value="Gets a cat picture", inline=False)
      cool.add_field(name="s.avatar [user]", value="Gets a user's avatar", inline=False)
      cool.add_field(name="s.servericon", value="Gets the server icon", inline=False)
      cool.add_field(name="s.ascii [value]", value="Converts text into ascii", inline=False)
      cool.add_field(name="s.urban [word]", value="Search a word on Urban Dictionnary", inline=False)
      await ctx.bot.say(embed=cool)
      
    @help.command(pass_context = True, no_pm = True)
    async def mod(ctx):  
      mod = discord.Embed(title="__Moderator commands!__", description="-", color=0x00ff00)
      mod.add_field(name="s.ban", value="Bans a certain user", inline=False)
      mod.add_field(name="s.unban", value="Unbans a certain user", inline=False)
      mod.add_field(name="s.kick", value="Kicks a certain user", inline=False)
      mod.add_field(name="s.softban", value="Softbans a certain user", inline=False)
      mod.add_field(name="s.clear [x]", value="Clears 'x' messages (Maximum of 100 at a time)", inline=False)
      mod.add_field(name="s.purge [x]", value="Kicks users who have been inactive since 'x' days (Maximum of 30)", inline=False)
      await ctx.bot.say(embed=mod)
      
    @help.command(pass_context = True, no_pm = True)
    async def support(ctx):
      support = discord.Embed(title="__Support commands!__", description="-", color=0x00ff00)
      support.add_field(name="s.report [bug]", value="Reports a bug to my dev team", inline=False)
      support.add_field(name="s.suggest [suggestion]", value="Sends a suggestion to the dev team", inline=False)
      support.add_field(name="s.mm [message]", value="Enters a DM with the bot dev's (Use this command in DM only)", inline=False)
      await ctx.bot.say(embed=support)
    
    @help.command(pass_context = True, no_pm = True)
    async def beta(ctx):
      beta = discord.Embed(title="__Beta commands!__", description="-", color=0x00ff00)
      beta.add_field(name="s.giveaway [seconds] [winners] [prize]", value="Creates a giveaway in the channel", inline=False)
      if ctx.message.author.id not in beta_ids:
        perm_error = discord.Embed(title=":warning: Error!",description="You do not have the permission to use this command",color=0xff0000)
        await ctx.bot.say(embed=perm_error)
      else:
        await ctx.bot.say(embed=beta)
        
    @help.command(pass_context=True, no_pm = True)
    async def image(ctx):
      support = discord.Embed(title="__Image commands!__", description="-", color=0x00ff00)
      support.add_field(name="s.blurple [image/user]", value="Makes an image blurple, if left empty, author's avatar will be used", inline=False)
      await ctx.bot.say(embed=support)
      
      

    @commands.command(pass_context = True, no_pm = True)
    async def suggest(ctx, *, suggests: str):
        embed = discord.Embed(title="__New suggestion!__", description="I have recieved a new suggestion !", color=0x00ff00)
        embed.add_field(name="Sent by", value=ctx.message.author, inline=True)
        embed.add_field(name="Suggestion", value=suggests, inline=True)
        embed.set_footer(text="From: {}".format(ctx.message.server), icon_url=ctx.message.server.icon_url)
        await ctx.bot.delete_message(ctx.message)
        await ctx.bot.send_message(suggest, embed=embed)
        await ctx.bot.say("Your suggestion has been sent to my dev team!")

    @commands.command(pass_context = True, no_pm = True)
    async def servers(ctx):
      
      serverCount = 0
      members = 0
      for server in ctx.bot.servers:
        serverCount += 1
        for member in server.members:
            members += 1
        
      embed = discord.Embed(title="Serving", description='{0} servers for {1} users'.format(serverCount, members), color=0x00ff00)
      await ctx.bot.say(embed=embed)
        
    @commands.command(pass_context = True, no_pm = True, aliases=["botinfo", "bi", "bot", "info", "about"])
    async def stats(ctx):
        RAM = psutil.virtual_memory()
        used = RAM.used >> 20
        percent = RAM.percent
        cpu = psutil.cpu_percent()
        os = platform.system()
        totalusers = 0
        totalchannels = 0
        onlineusers = 0
        humans = 0
        bots = 0
        serverCount = 0
        members = 0
        channels = []
        embed = discord.Embed(title="Here are my stats!", color = 0x000000)
        embed.set_thumbnail(url=ctx.message.server.me.avatar_url)
        embed.add_field(name="Author", value="Waba#8929")
        embed.add_field(name="Total Servers", value=len(ctx.bot.servers))
        embed.add_field(name="CPU", value="{}%".format(cpu))
        embed.add_field(name="RAM", value="2.37% (94.8MB)")
        embed.add_field(name="Discord.py Version", value=discord.__version__)
        embed.add_field(name="Python Version", value=platform.python_version())
        await ctx.bot.say(embed=embed)
        
    @commands.command(pass_context = True, no_pm = True, aliases = ["id", "userid"])
    async def getid(ctx, *, member: discord.Member = None):
      if member is None:
        embed = discord.Embed(title="Your id is:", description=ctx.message.author.id, color=0x000000)
      else:
        embed = discord.Embed(title="{}'s id is:".format(member), description=member.id, color=0x000000)
      await ctx.bot.say(embed=embed)
      
    @commands.command(pass_context = True, no_pm = True, aliases=["ui", "user"])
    async def userinfo(ctx, *, member: discord.Member = None):
      if member is None:
        user = ctx.message.author
      else:
        user = member
      ago = (ctx.message.timestamp - user.joined_at).days
      account_ago = (ctx.message.timestamp - user.created_at).days
      msg = []
      for role in user.roles:
        msg.append(role.mention)
      msg.pop(0)
      msg.insert(0, '@everyone')
      if user.status == 'online':
        status = ""
      userinfo = discord.Embed(title="{}'s info".format(user.name), description="Known As : {}".format(user.nick), color = 0x000000)
      userinfo.set_thumbnail(url=user.avatar_url)
      userinfo.add_field(name="ID:", value=user.id)
      userinfo.add_field(name="Is Bot?:", value=user.bot)
      userinfo.add_field(name="Playing:", value=user.game)
      userinfo.add_field(name="Status:", value=user.status)
      userinfo.add_field(name="Joined Server:", value="***{0}***, about {1} days ago".format(str(user.joined_at.strftime("%A, %b %d, %Y")), ago))
      userinfo.add_field(name="Account Created:", value="***{0}***, about {1} days ago".format(str(user.created_at.strftime("%A, %b %d, %Y")), account_ago))
      userinfo.add_field(name="Roles:", value=" **|** ".join(msg))
      userinfo.set_footer(text="Requested by {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
      
      await ctx.bot.say(embed = userinfo)
      
        
    @commands.command(pass_context = True, no_pm = True)
    async def serverlist(ctx):
      server_list = []
      try:
        for server in ctx.bot.servers:
          server_list.append(server.name)
        await ctx.bot.say('\n'.join(server_list))
      except:
        todo = discord.Embed(title=":warning: Error!",description="The bot is in too many servers to show them all",color=0xff0000)
        await ctx.bot.say(embed = todo)
    
    @commands.command(pass_context = True, no_pm = True, aliases=["perms", "perm"])
    async def permissions(ctx, member: discord.Member=None):
      if member is None:
        user= ctx.message.author
      else:
        user= member
      up = user.server_permissions
      perm_list=['Is administrator: {} '.format(up.administrator), 'Can Manage Emojis: {} '.format(up.manage_emojis), 'Can Manage Webhooks: {} '.format(up.manage_webhooks), 'Can Change Nickname: {} '.format(up.change_nickname), 'Can Move Members: {} '.format(up.move_members), 'Can Deafen Members: {} '.format(up.deafen_members), 'Can Mute Members: {} '.format(up.mute_members), 'Can Speak in Voice Channels: {} '.format(up.speak), 'Can Connect to Voice Channels: {} '.format(up.connect), 'Can Use External Emojis: {} '.format(up.external_emojis), 'Can Read Message History: {} '.format(up.read_message_history), 'Can Attach Files: {} '.format(up.attach_files), 'Can Embed Links: {} '.format(up.embed_links), 'Can View Audit Log: {} '.format(up.view_audit_logs), 'Can Send TTS Messages: {} '.format(up.send_tts_messages), 'Can Send Messages: {} '.format(up.send_messages), 'Can Read Messages: {} '.format(up.read_messages), 'Can Add Reactions: {} '.format(up.add_reactions), 'Can Manage Roles: {} '.format(up.manage_roles), 'Can Manage Nicknames: {} '.format(up.manage_nicknames), 'Can Manage Server: {} '.format(up.manage_server), 'Can Manage Messages: {} '.format(up.manage_messages), 'Can Manage Channels: {} '.format(up.manage_channels), 'Can Mention Everyone: {} '.format(up.mention_everyone), 'Can Create Invite: {} '.format(up.create_instant_invite), 'Can Kick Members: {} '.format(up.kick_members), 'Can Ban Members: {} '.format(up.ban_members)]
      em = discord.Embed(title="Server Permissions for {}".format(str(user)),color=user.color)
      message = 'Is Owner: {}'.format(ctx.message.server.owner == user)
      for x in perm_list:
        message += "\n" + x
      em.set_thumbnail(url=user.avatar_url)
      em = discord.Embed(title="Server Permissions for {}".format(str(user)),description=message, color=user.color)
      em.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
      em1 = await ctx.bot.say(embed=em)
      await asyncio.sleep(30)
      await ctx.bot.delete_message(em1)
      await ctx.bot.delete_message(ctx.message)
    
    @bot.command(pass_context=True)
    async def charinfo(ctx, characters=None):
      if characters is None:
        todo = discord.Embed(title=":warning: Error!",description="`emoji` is a required argument",color=0xff0000)
        await ctx.bot.say(embed = todo)
      else:
        if len(characters) > 10:
          return await ctx.bot.say(f"**:x:  |  Tooooo many characters. ({len(characters)}/10)**")

        def to_string(c):
          digit = f'{ord(c):x}'
          name = unicodedata.name(c, "**:x:  |  Emoji name not found.**")
          return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'

        await ctx.bot.say("\n".join(map(to_string, characters)))
        
    @bot.command(pass_context = True, aliases = ["mems"])
    async def members(ctx):
        online = 0
        idle = 0
        dnd = 0
        offline = 0
        bots = 0
        humans = 0
        total = 0
        for mems in ctx.message.server.members:
                lm = str(mems.status)
                if str(lm) == 'online':
                        online += 1
                elif str(lm) == 'idle':
                        idle += 1
                elif str(lm) == 'dnd':
                        dnd += 1
                else:
                        offline += 1
                if mems.bot is True:
                  bots += 1
                  total += 1
                else:
                  humans += 1
                  total += 1
        em= discord.Embed(title='Server Members', description = '**Members:** {} humans | {} bots | {} total\n**Member Statuses:** <:online:313956277808005120> `{}` | <:away:313956277220802560> `{}` | <:dnd:313956276893646850> `{}` | <:offline:313956277237710868> `{}`'.format(humans, bots, total, online, idle, dnd, offline))
        await ctx.bot.say(embed = em)
        
        
      
        
def setup(bot):
    bot.add_cog(Utils)
