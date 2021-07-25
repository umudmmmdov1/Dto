import os, requests, re
import asyncio
import time
from datetime import datetime
from userbot import SUDO_ID
from telethon.errors import ChannelInvalidError as cie
from io import BytesIO
from telethon import types, events
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.types import *
from telethon.tl.functions.messages import SendMediaRequest
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from userbot import bot

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("extra")

# ████████████████████████████████ #

@register(pattern="^.ttext", outgoing=True)
async def doc2text(event):
    doc = await event.client.download_media(await event.get_reply_message())
    fayl = open(doc, "r")
    readed = fayl.read()
    fayl.close()
    fayl = await event.reply("(LANG['T1'])")
    if len(readed) >= 4096:            
            await event.edit("(LANG['T2'])")
            out = readed
            url = "https://del.dog/documents"
            r = requests.post(url, data=out.encode("UTF-8")).json()
            url = f"https://del.dog/{r['key']}"
            await event.edit(
                f"(LANG['T3'])", link_preview=False)            
            await fayl.delete()
    else:
        await event.client.send_message(event.chat_id, f"{readed}")
        await fayl.delete()
        await event.delete()
    os.remove(doc)
    
    
@register(outgoing=True, pattern="^.tdoc ?(.*)")
async def text2doc(event):
    metn = event.text[5:]
    if metn is None:
        await event.edit("`Bir mətnə cavab verin`. \n**Məsələn:** `.tdoc <fayl adı>`")
        return
    cvb = await event.get_reply_message()
    if cvb.text:
        with open(metn, "w") as fayl:
            fayl.write(cvb.message)
        await event.delete()
        await event.client.send_file(event.chat_id, metn, caption="[U S Σ R Δ T O R](t.me/UseratorSUP)", force_document=True)
        os.remove(metn)
    else:
        await event.edit("`Bir mətnə cavab verin`. \n**Məsələn:** `.tdoc <fayl adı>`")


@register(outgoing=True, pattern="^.ftoi")
async def f2i(event):
    await event.delete()
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  
    if image.mime_type == 'image/webp':
        return 
    if image.size > 10 * 1024 * 1024:
        return 

    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = 'image.png'

    try:
        await event.client(SendMediaRequest(
            peer=await event.get_input_chat(),
            media=types.InputMediaUploadedPhoto(img),
            message=target.message,
            entities=target.entities,
            reply_to_msg_id=target.id
        ))
    except PhotoInvalidDimensionsError:
        return


@register(outgoing=True, pattern="^.post (.*)")
@register(incoming=True, from_users=SUDO_ID, pattern="^.post (.*)")
async def send(event):
        args = event.pattern_match.group(1)
        mesaj = await event.get_reply_message()
        if not args:
          await event.edit("Göndərəcək kanal seçin")
        try: kanal = await event.client.get_input_entity(int(args) if re.match(r'-{0,1}\d+', args) else args)
        except cie:
          await event.edit(f"Belə bir kanal və ya qrup yoxdu\nXəta: {cie}")
        except Exception as e:
          await event.edit(f"Xəta: {e}")
        v = await event.client.send_message(kanal, mesaj)
        await event.edit(f"Mesaj {args} kanal/qrupuna göndərildi!")


@register(outgoing=True, pattern="^.statis")
async def stats(e): 
   await e.edit("`Məlumatlar toplanılır...`") 
   msg = str((await e.client.get_messages(e.chat_id, limit=0)).total) 
   img = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterPhotos())).total) 
   vid = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterVideo())).total)
   msc = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterMusic())).total)
   ses = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterVoice())).total)
   rvid = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterRoundVideo())).total) 
   doc = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterDocument())).total) 
   url = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterUrl())).total) 
   gif = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterGif())).total) 
   geo = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterGeo())).total) 
   kntk = str((await e.client.get_messages(e.chat_id, limit=0, filter=InputMessagesFilterContacts())).total) 
   
   stat = f"✉️ **Mesajlar:** `{msg}`\n🖼️ **Fotolar:** `{img}`\n📹 **Videolar:** `{vid}`\n🎵 **Musiqilər:** `{msc}`\n🎤 **Səsli mesajlar:** `{ses}`\n🎥 **Video Notlar:** `{rvid}`\n📂 **Fayllar:** `{doc}`\n🔗 **Linklər:** `{url}`\n🎞️ **GIF'lər:** `{gif}`\n🗺 **Yerlər:** `{geo}`\n🛂 **Kontaktlar:** `{kntk}`"
   await e.edit(stat)


CmdHelp('extra').add_command(
  'ttext', None, 'Cavab verdiyiniz faylı yazıya çevirər'
).add_command(
  'tdoc', '<fayl adı>', 'Cavab verdiyiniz mətni verdiyiniz addakı fayla çevirər'
).add_command(
  'ftoi', None, 'Cavab verdiyiniz faylı şəkilə çevirər'
).add_command(
  'post', '<göndəriləcək kanal> <cavab mesaj>', 'Cavab verdiyiniz mesajı istədiyiniz kanal/qrupa göndərər'
).add_command('statis',  None, 'Söhbət haqqında ətraflı məlumat alın').add()
