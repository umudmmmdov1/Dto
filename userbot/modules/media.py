from PIL import Image, ImageDraw, ImageOps, ImageFilter 
from userbot import bot
import io, os
from telethon.tl.types import DocumentAttributeFilename 
from userbot.modules import MEDIACHECK
from moviepy.editor import VideoFileClip
from userbot.events import register
 
 
@register(outgoing=True, pattern="^.round")
async def rounder(event):
  reply = None 
  if event.is_reply: 
   reply = await event.get_reply_message()
   data = await MEDIACHECK(reply) 
   if isinstance(data, bool): 
    await event.edit("Bir şəkil/sticker/video və ya gif'ə cavab verin") 
    return 
  else: 
   await event.edit("Bir şəkil/sticker/video və ya gif'ə cavab verin")
   return 
  data, type = data 
  if type == "img": 
   await event.edit("📷 Şəkil hazırlanır") 
   img = io.BytesIO() 
   bytes = await bot.download_file(data, img) 
   im = Image.open(img) 
   w, h = im.size 
   img = Image.new("RGBA", (w,h), (0,0,0,0)) 
   img.paste(im, (0, 0)) 
   m = min(w, h) 
   img = img.crop(((w-m)//2, (h-m)//2, (w+m)//2, (h+m)//2)) 
   w, h = img.size 
   mask = Image.new('L', (w, h), 0) 
   draw = ImageDraw.Draw(mask)  
   draw.ellipse((10, 10, w-10, h-10), fill=255) 
   mask = mask.filter(ImageFilter.GaussianBlur(2)) 
   img = ImageOps.fit(img, (w, h)) 
   img.putalpha(mask) 
   skl = io.BytesIO() 
   skl.name = "img.webp" 
   img.save(skl) 
   skl.seek(0) 
   await event.client.send_file(event.chat_id, skl, reply_to=reply) 
  else: 
   await event.edit("🎥 Video hazırlanır") 
   await bot.download_file(data, "video.mp4") 
   video = VideoFileClip("video.mp4") 
   video.reader.close() 
   w, h = video.size 
   m = min(w, h) 
   box = [(w-m)//2, (h-m)//2, (w+m)//2, (h+m)//2] 
   video = video.crop(*box) 
   await event.edit("📼 Video göndərilir...") 
   video.write_videofile("userator.mp4") 
   await event.client.send_file(event.chat_id, "userator.mp4", video_note=True, reply_to=reply) 
   os.remove("video.mp4") 
   os.remove("userator.mp4") 
  await event.delete() 
    
