# U S Σ R Δ T O R / Ümüd

""" Stickers """
import asyncio, time, random
import io, os, re, requests
import math
import urllib.request
from os import remove
from bs4 import BeautifulSoup
from asyncio import sleep
from datetime import datetime
from io import BytesIO
from PIL import Image
from telethon import functions, types, events
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto, InputPeerNotifySettings,InputStickerSetID, DocumentAttributeSticker
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest, SendMediaRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot, PAKET_ISMI, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from userbot.cmdhelp import CmdHelp


PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."
PACK_DOESNT_EXIST = "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, "", inputString)



# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("stickers")

# ████████████████████████████████ #


@register(outgoing=True, pattern="^.fırlat($| )?((?![0-9]).+?)? ?([0-9]*)?")
async def fırlat(event):
    await event.edit(f"`{PLUGIN_MESAJLAR['dızcı']}`")
    user = await bot.get_me()
    pack_username = ''
    if not user.username:
        try:
            user.first_name.decode('ascii')
            pack_username = user.first_name
        except UnicodeDecodeError: 
            pack_username = user.id
    else: pack_username = user.username

    textx = await event.get_reply_message()
    emoji = event.pattern_match.group(2)
    number = int(event.pattern_match.group(3) or 1) 
    new_pack = False

    if textx.photo or textx.sticker: message = textx
    elif event.photo or event.sticker: message = event
    else:
        await event.edit(LANG['GIVE_STICKER'])
        return

    sticker = io.BytesIO()
    await bot.download_media(message, sticker)
    sticker.seek(0)

    if not sticker:
        await event.edit(LANG['FAIL_DOWNLOAD'])
        return

    is_anim = message.file.mime_type == "application/x-tgsticker"
    if not is_anim:
        img = await resize_photo(sticker)
        sticker.name = "sticker.png"
        sticker.seek(0)
        img.save(sticker, "PNG")

  
    if not emoji:
        if message.file.emoji: 
            emoji = message.file.emoji
        else: 
            emoji = "🤔"

    packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
    packtitle = (f"@{user.username or user.first_name} {PAKET_ISMI} "
                f"{number}{' animasyonlu' if is_anim else ''}")
    response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
    htmlstr = response.read().decode("utf8").split('\n')
    new_pack = PACK_DOESNT_EXIST in htmlstr

    if new_pack:
        await event.edit(LANG['NEW_PACK'])
        await newpack(is_anim, sticker, emoji, packtitle, packname, message)
    else:
        async with bot.conversation("Stickers") as conv:
            await conv.send_message('/cancel')
            await conv.get_response()
            await conv.send_message('/addsticker')
            await conv.get_response()

            await conv.send_message(packname)
            x = await conv.get_response()

            while x.text == PACK_FULL:
                number += 1
                packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
                packtitle = (f"@{user.username or user.first_name} {PAKET_ISMI} "
                            f"{number}{' animated' if is_anim else ''}")

                await event.edit(
                    LANG['TOO_STICKERS'].format(number)
                )

                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text == "Invalid pack selected.": 
                    await newpack(is_anim, sticker, emoji, packtitle, packname)
                    await bot.send_read_acknowledge("stickers")
                    muted = await bot(UpdateNotifySettingsRequest(
                        peer=429000,
                        settings=InputPeerNotifySettings(mute_until=None))
                    )

                    await event.edit(
                        f"`Stiker {number}{'(animasyonlu)' if is_anim else ''} sayılı paketə əlavə edildi, "
                        f"{emoji} emojisi ilə birlikdə! "
                        f"Paket `[burada](t.me/addstickers/{packname})`tapa bilərsiz.`",
                        parse_mode='md')
                    return

            # Upload the sticker file
            if is_anim:
                upload = await message.client.upload_file(sticker, file_name="AnimatedSticker.tgs")
                await conv.send_file(upload, force_document=True)
            else:
                sticker.seek(0)
                await conv.send_file(sticker, force_document=True)
            kontrol = await conv.get_response()
        
            if "Sorry, the image dimensions are invalid." in kontrol.text:
                await event.edit("`Sticker's kabul etmedi. İkinci yöntem deneniyor...`")
                try:
                    await bot.send_file("@ezstickerbot", message, force_document=True)
                except YouBlockedUserError:
                    return await event.edit("`Xaiş` @EzStickerBot `əngəldən çıxardın və təkrar cəhd edin!`")

                try:
                    response = await conv.wait_event(events.NewMessage(incoming=True,from_users=350549033))
                    if "Please temporarily use" in response.text:
                        await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                        response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                
                    await bot.send_read_acknowledge(350549033)
                    await event.client.forward_messages("stickers", response.message, 350549033)
                except:
                    await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                    response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                    await bot.send_read_acknowledge(891811251)
                    await event.client.forward_messages("stickers", response.message, 891811251)

            # Send the emoji
            await conv.send_message(emoji)
            await conv.get_response()

            # Finish editing the pack
            await conv.send_message('/done')
            await conv.get_response()

    # Read all unread messages
    await bot.send_read_acknowledge(429000)
    # Unmute Stickers bot back
    muted = await bot(UpdateNotifySettingsRequest(
        peer=429000,
        settings=InputPeerNotifySettings(mute_until=None))
    )

    await event.edit(
        f"`Stiker {number}{'(animasyonlu)' if is_anim else ''} saylı paketə əlavə edildi, "
        f"{emoji} emojisi ilə birlikdə! "
        f"Paket `[burada](t.me/addstickers/{packname})` tapa bilərsiz.`",
        parse_mode='md')


async def newpack(is_anim, sticker, emoji, packtitle, packname, message):
    async with bot.conversation("stickers") as conv:
      
        await conv.send_message('/cancel')
        await conv.get_response()

    
        if is_anim:
            await conv.send_message('/newanimated')
        else:
            await conv.send_message('/newpack')
        await conv.get_response()

      
        await conv.send_message(packtitle)
        await conv.get_response()

    
        if is_anim:
            upload = await bot.upload_file(sticker, file_name="AnimatedSticker.tgs")
            await conv.send_file(upload, force_document=True)
        else:
            sticker.seek(0)
            await conv.send_file(sticker, force_document=True)
        kontrol = await conv.get_response()
        if kontrol.message.startswith("Sorry"):
            await bot.send_file("@ezstickerbot", message, force_document=True)
            try:
                response = await conv.wait_event(events.NewMessage(incoming=True,from_users=350549033))
                if "Please temporarily use" in response.text:
                    await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                    response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                
                    await bot.send_read_acknowledge(350549033)
                    await bot.forward_messages("stickers", response.message, 350549033)
            except:
                await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                response = await conv.wait_event(events.NewMessage(incoming=True,from_users=891811251))
                await bot.send_read_acknowledge(891811251)
                await bot.forward_messages("stickers", response.message, 891811251)

     
        await conv.send_message(emoji)
        await conv.get_response()

       
        await conv.send_message("/publish")
        if is_anim:
            await conv.get_response()
            await conv.send_message(f"<{packtitle}>")
        await conv.get_response()

 
        await conv.send_message("/skip")
        await conv.get_response()
        
        await conv.send_message(packname)
        await conv.get_response()

async def resize_photo(photo):
    image = Image.open(photo)
    scale = 512 / max(image.width, image.height)
    new_size = (int(image.width*scale), int(image.height*scale))
    image = image.resize(new_size, Image.ANTIALIAS)
    return image


@register(outgoing=True, pattern="^.sinfo$")
async def get_pack_info(event):
    if not event.is_reply:
        return await event.edit("`Heç birşey haqqında məlumat verə bilmərəm :/`")

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await event.edit("`Yalnız stickerlər haqqında məlumat verə bilirəm...`")

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        await event.edit(
            "`Məlumatlar gətirilir...`")
    except BaseException:
        return await event.edit("`Bu bir sticker deyil. Bir stickerə cavab verin`")

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await event.edit("`Bu bir sticker deyil. Bir stickerə cavab verin`")

    get_stickerset = await bot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash)))
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"**Paket Başlığı:** `{get_stickerset.set.title}\n`"
        f"**Paketin Qısa adı:** `{get_stickerset.set.short_name}`\n"
        f"**Rəsmi:** `{get_stickerset.set.official}`\n"
        f"**Arxiv:** `{get_stickerset.set.archived}`\n"
        f"**Paketdəki emojili sticker sayı:** `{len(get_stickerset.packs)}`\n"
        f"**Paketdəki emojilər:**\n{' '.join(pack_emojis)}"
    )

    await event.edit(OUTPUT)


@register(outgoing=True, pattern="^.spng$")
async def sticker_to_png(sticker):
    if not sticker.is_reply:
        await sticker.edit("`NULL information to fetch...`")
        return False

    img = await sticker.get_reply_message()
    if not img.document:
        await sticker.edit("`Bir stickerə cavab verin`")
        return False

    try:
        img.document.attributes[1]
    except Exception:
        await sticker.edit("`Bu bir sticker deyil`")
        return

    with io.BytesIO() as image:
        await sticker.client.download_media(img, image)
        image.name = 'sticker.png'
        image.seek(0)
        try:
            await img.reply(file=image, force_document=True)
        except Exception:
            await sticker.edit("**Xəta:** `faylı göndərə bilmədim...`")
        else:
            await sticker.delete()
    return

@register(outgoing=True, pattern=".stik ?(.*)")
async def itos(event):
    if event.fwd_from:
        return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    event = await event.edit("__Çevrilir...___")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.webp"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = TEMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("`Çevirə bilmədim`")
    else:
        await event.edit("**Cavab verdiyiniz şəkili stickerə çevirər**")

@register(outgoing=True, pattern=r"^\.q2(?: |$)(.*)")
async def rastick(event):
    text = event.pattern_match.group(1)
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            await event.answer("`Mətin daxil edilmədi stiker ola bilməz.`")
            return
    animus = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    try:
        await sticcers[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            silent=True if event.is_reply else False,
            hide_via=True,
        )
    except Exception:
        return await event.edit(
            "`Bu söhbətdə sətir içi nəticələr göndərə bilməzsiniz (caused by SendInlineBotResultRequest)`"
        )
    await sleep(2)
    await event.delete()

@register(outgoing=True, pattern=r"^.spack (.*)")
async def search_pack(event):
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("`Axtardığınız paketin adını daxil edin`")
    await event.edit("`Axtarılır...`")
    text = requests.get("https://combot.org/telegram/stickers?q=" + query).text
    soup = BeautifulSoup(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        return await event.edit("**Nəticə tapılmadı**")
    netice = f"**Axtarış:**\n `{query}`\n\n**Nəticələr:**\n"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            netice += f" ➤ [{packtitle}]({packlink})\n\n"
    await event.edit(netice)


CmdHelp('stickers').add_command(
    'fırlat', None, (LANG['STIK1'])
).add_command(
    'sinfo', None, 'Stiker haqqında məlumat verər.'
).add_command(
    'spng', None, 'Stikeri png kimi göndərər.'
).add_command(
    'stik', None, 'Fırlat əmrindən fərqli olaraq stickeri paket yaratmadan göndərər.'
).add_command(
    'q2',  '<söz>', 'Yazıları maraqlı stikerlərə çevirər'
).add_command(
    'q', '<rəqəm>', 'Yazını stikerə çevirər'
).add_command(
    'spack', '<söz>', 'Stiker paketi axtarışı edər'
).add()
