# U S Σ R Δ T O R / Ümüd

from userbot.cmdhelp import CmdHelp
from userbot import PLUGIN_CHANNEL_ID, CMD_HELP
from userbot.events import register
from re import search
from json import loads, JSONDecodeError
from userbot.language import LANGUAGE_JSON
from os import remove

@register(outgoing=True, pattern="^.dil ?(.*)")
async def dil(event):
    global LANGUAGE_JSON

    komut = event.pattern_match.group(1)
    if search(r"y[uü]kle|install", komut):
        await event.edit("`Dil faylı yüklənir... Xahiş gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            dosya = await reply.download_media()

            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "dtojson")):
                return await event.edit("`Xaiş keçərli bir` **DTOJSON** `faylı verin!`")

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xaiş keçərli bir` **DTOJSON** `faylı verin!`")

            await event.edit(f"`{dosya['LANGUAGE']}` `dili yüklənir...`")
            pchannel = await event.client.get_entity(PLUGIN_CHANNEL_ID)

            dosya = await reply.download_media(file="./userbot/language/")
            dosya = loads(open(dosya, "r").read())
            await reply.forward_to(pchannel)
            
            LANGUAGE_JSON = dosya
            await event.edit(f"✅ `{dosya['LANGUAGE']}` `dili uğurla yükləndi!`\n\n**İstəklərin keçərli olması üçün botu yenidən başladın!**")
        else:
            await event.edit("**Xaiş bir dil faylına cavab olaraq yazın!**")
    elif search(r"melumat|info", komut):
        await event.edit("`Dil faylı məlumatları gətirilir... Xaiş gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "dtojson")):
                return await event.edit("`Xaiş keçərli bir` **DTOJSON** `faylı verin!`")

            dosya = await reply.download_media()

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xaiş keçərli bir` **DTOJSON** `faylı verin!`")

            await event.edit(
                f"**Dil: **`{dosya['LANGUAGE']}`\n"
                f"**Dil Kodu: **`{dosya['LANGCODE']}`\n"
                f"**Tərcüməçi: **`{dosya['AUTHOR']}`\n"

                f"\n\n`Dil faylını yükləmək üçün` `.dil yükle` `əmrini işlədin.`"
            )
        else:
            await event.edit("**Xaiş bir dil faylına cavab olaraq yazın!**")
    else:
        await event.edit(
            f"**Dil: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Dil Kodu: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Tərcüməçi: **`{LANGUAGE_JSON ['AUTHOR']}`\n"

            f"\n\nDigər dillər üçün @UseratorLang kanalına baxa bilərsiz."
        )

CmdHelp('dil').add_command(
    'dil', None, 'Yüklədiyiniz dil haqqında məlumat verər.'
).add_command(
    'dil melumat', None, 'Cavab verdiyiniz dil faylı haqqında məlumat verər.'
).add_command(
    'dil yükle', None, 'Cavab verdiyiniz dil faylını yükləyər.'
).add()
