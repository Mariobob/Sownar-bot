
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
from PIL import Image, ImageEnhance, ImageSequence
import PIL
from io import BytesIO
import io
import datetime
import aiohttp
import copy
import sys
import time
from resizeimage import resizeimage
import math
  
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

class Image():
    print('image loaded')
    print('------')
    
    @commands.command(pass_context = True)
    @commands.cooldown(rate=1, per=30, type=BucketType.user)
    async def blurple(ctx, arg1 = None):
      picture = None

      await ctx.bot.send_typing(ctx.message.channel)

      start = time.time()
      if arg1 != None:
        if "<@!" in arg1:
            arg1 = arg1[:-1]
            arg1 = arg1[3:]
        if "<@" in arg1:
            arg1 = arg1[:-1]
            arg1 = arg1[2:]
        if arg1.isdigit() == True:
            try:
                user = await bot.get_user_info(int(arg1))
                picture = user.avatar_url
            except Exception:
                pass
        else:
            picture = arg1
      else:
        link = ctx.message.attachments
        if len(link) != 0:
            for image in link:
                picture = image.url

      if picture == None:
        picture = ctx.message.author.avatar_url

      try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get(picture) as r:
                response = await r.read()
      except ValueError:
        await ctx.send(f"{ctx.message.author.display_name}, please link a valid image URL")
        return

      colourbuffer = 20

      try:
        im = Image.open(BytesIO(response))
      except Exception:
        await ctx.send(f"{ctx.message.author.display_name}, please link a valid image URL")
        return

      imsize = list(im.size)
      impixels = imsize[0]*imsize[1]
      #1250x1250 = 1562500
      maxpixelcount = 1562500

      try:
        i = im.info["version"]
        isgif = True
        gifloop = int(im.info["loop"])
      except Exception:
        isgif = False


    

      end = time.time()
 
      start = time.time()
      if impixels > maxpixelcount:
        downsizefraction = math.sqrt(maxpixelcount/impixels)
        im = resizeimage.resize_width(im, (imsize[0]*downsizefraction))
        imsize = list(im.size)
        impixels = imsize[0]*imsize[1]
        end = time.time()
        #await ctx.send(f'{ctx.message.author.display_name}, image resized smaller for easier processing ({end-start:.2f}s)')
        start = time.time()

      def imager(im):
        im = im.convert(mode='L')
        im = ImageEnhance.Contrast(im).enhance(1000)
        im = im.convert(mode='RGB')

        img = im.load()

        for x in range(imsize[0]-1):
            i = 1
            for y in range(imsize[1]-1):
                pixel = img[x,y]

                if pixel != (255, 255, 255):
                    img[x,y] = (114, 137, 218)

        image_file_object = io.BytesIO()
        im.save(image_file_object, format='png')
        image_file_object.seek(0)
        return image_file_object

      def gifimager(im, gifloop):
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
        newgif = []

        for frame in frames:

            frame = frame.convert(mode='L')
            frame = ImageEnhance.Contrast(frame).enhance(1000)
            frame = frame.convert(mode='RGB')

            img = frame.load()

            for x in range(imsize[0]):
                i = 1
                for y in range(imsize[1]):
                    pixel = img[x,y]

                    if pixel != (255, 255, 255):
                        img[x,y] = (114, 137, 218)

            newgif.append(frame)

        image_file_object = io.BytesIO()

        gif = newgif[0]
        gif.save(image_file_object, format='gif', save_all=True, append_images=newgif[1:], loop=0)

        image_file_object.seek(0)
        return image_file_object


      with aiohttp.ClientSession() as session:
        start = time.time()
        if isgif == False:
            image = await bot.loop.run_in_executor(None, imager, im)
        else:
            image = await bot.loop.run_in_executor(None, gifimager, im, gifloop)
        end = time.time()
        if isgif == False:
            image = discord.File(fp=image, filename='image.png')
        else:
            image = discord.File(fp=image, filename='image.gif')

        try:
            embed = discord.Embed(Title = "", colour = 0x7289DA)
            if isgif == False:
                embed.set_image(url="attachment://image.png")
          
            else:
                embed.set_image(url="attachment://image.gif")
            embed.set_thumbnail(url=picture)
            await ctx.bot.say(embed=embed, file=image)
        except Exception:
            await ctx.bot.say("Error loading image, it is too big!")

    
    
def setup(bot):
    bot.add_cog(Image)
