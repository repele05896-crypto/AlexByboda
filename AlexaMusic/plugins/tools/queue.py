# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


import asyncio
import os
from random import randint

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message

import config
from config import BANNED_USERS
from strings import get_command
from AlexaMusic import app
from AlexaMusic.misc import db
from AlexaMusic.utils import Alexabin, get_channeplayCB, seconds_to_min
from AlexaMusic.utils.database import get_cmode, is_active_chat, is_music_playing
from AlexaMusic.utils.decorators.language import language, languageCB
from AlexaMusic.utils.inline import queue_back_markup, queue_markup

###Commands
QUEUE_COMMAND = get_command("QUEUE_COMMAND")

basic = {}


def get_image(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"
    else:
        return config.YOUTUBE_IMG_URL


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "Unknown"
    duration_seconds = int(playing[0]["seconds"])
    return "Unknown" if duration_seconds == 0 else "Inline"


@app.on_message(filters.command(QUEUE_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text("🍒 تـأكـد مـن ربـط الـقـنـاة بـالـمـجـمـوعـة أولاً.")
        try:
            await app.get_chat(chat_id)
        except Exception:
            return await message.reply_text("🍒 فـشـل فـي الـحـصـول عـلـى مـعـلـومـات الـقـنـاة، تـأكـد أن الـبـوت مـشـرف هـنـاك.")
        cplay = True
    else:
        chat_id = message.chat.id
        cplay = False
    if not await is_active_chat(chat_id):
        return await message.reply_text("🍒 مـفـيـش مـكـالـمـة صـوتـيـة شـغـالـة حـالـيـاً فـي الـجـروب ده.")
    got = db.get(chat_id)
    if not got:
        return await message.reply_text("🍒 قـائـمـة الانـتـظـار فـارغـة، مـفـيـش أغـانـي شـغـالـة.")
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = (
                config.TELEGRAM_AUDIO_URL
                if typo == "Audio"
                else config.TELEGRAM_VIDEO_URL
            )
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)
    send = (
        "**🤍 الـمـدة:** بـث مـبـاشـر (غـيـر مـحـدد)\n\nاضـغـط عـلـى الـزر بـالأسـفـل لـعـرض الـقـائـمـة كـامـلـة."
        if DUR == "Unknown"
        else "\nاضـغـط عـلـى الـزر بـالأسـفـل لـعـرض الـقـائـمـة كـامـلـة."
    )
    cap = f"""**{config.MUSIC_BOT_NAME} 🧚**

☔ **الاسـم:** {title}

🧚 **الـنـوع:** {typo}
💕 **طـلـب بـواسـطـة:** {user}
{send}"""
    upl = (
        queue_markup(_, DUR, "c" if cplay else "g", videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            "c" if cplay else "g",
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True
    mystic = await message.reply_photo(IMAGE, caption=cap, reply_markup=upl)
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if not await is_active_chat(chat_id):
                    break
                if basic[videoid]:
                    if await is_music_playing(chat_id):
                        try:
                            buttons = queue_markup(
                                _,
                                DUR,
                                "c" if cplay else "g",
                                videoid,
                                seconds_to_min(db[chat_id][0]["played"]),
                                db[chat_id][0]["dur"],
                            )
                            await mystic.edit_reply_markup(reply_markup=buttons)
                        except FloodWait:
                            pass
                else:
                    break
        except Exception:
            return


@app.on_callback_query(filters.regex("GetTimer") & ~BANNED_USERS)
async def quite_timer(client, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except Exception:
        pass


@app.on_callback_query(filters.regex("GetQueued") & ~BANNED_USERS)
@languageCB
async def queued_tracks(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    try:
        chat_id, channel = await get_channeplayCB(_, what, CallbackQuery)
    except Exception:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("🍒 مـفـيـش مـكـالـمـة صـوتـيـة شـغـالـة حـالـيـاً.", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("🍒 قـائـمـة الانـتـظـار فـارغـة.", show_alert=True)
    if len(got) == 1:
        return await CallbackQuery.answer("🍒 مـفـيـش غـيـر الأغـنـيـة دي بـس الـلـي شـغـالـة، مـفـيـش حـاجـة فـي الانـتـظـار.", show_alert=True)
    await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(_, what)
    med = InputMediaPhoto(
        media="https://files.catbox.moe/b6533n.jpg",
        caption="🤍 دي قـائـمـة الأغـانـي الـلـي فـي الانـتـظـار يـا غـالـي.",
    )
    await CallbackQuery.edit_message_media(media=med)
    msg = ""
    for j, x in enumerate(got, start=1):
        if j == 1:
            msg += f'🧚 **مـشـغـل الآن:**\n\n☔ الاسـم: {x["title"]}\n🤍 الـمـدة: {x["dur"]}\n💕 بـواسـطـة: {x["by"]}\n\n'
        elif j == 2:
            msg += f'🧚 **فـي الانـتـظـار:**\n\n☔ الاسـم: {x["title"]}\n🤍 الـمـدة: {x["dur"]}\n💕 بـواسـطـة: {x["by"]}\n\n'
        else:
            msg += f'☔ الاسـم: {x["title"]}\n🤍 الـمـدة: {x["dur"]}\n💕 بـواسـطـة: {x["by"]}\n\n'
    if "Queued" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)
        if "☔" in msg:
            msg = msg.replace("☔", "")
        link = await Alexabin(msg)
        med = InputMediaPhoto(media=link, caption=f"🤍 الـقـائـمـة طـويـلـة جـداً، تـقـدر تـشـوفـهـا مـن هـنـا:\n{link}")
        await CallbackQuery.edit_message_media(media=med, reply_markup=buttons)
    else:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex("queue_back_timer") & ~BANNED_USERS)
@languageCB
async def queue_back(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cplay = callback_data.split(None, 1)[1]
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except Exception:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("☔ مـفـيـش مـكـالـمـة صـوتـيـة شـغـالـة حـالـيـاً.", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("🤍 الـقـائـمـة فـارغـة.", show_alert=True)
    await CallbackQuery.answer("🧚 لـحـظـة واحـدة، راجـعـيـن لـلـمـشـغـل...", show_alert=True)
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = (
                config.TELEGRAM_AUDIO_URL
                if typo == "Audio"
                else config.TELEGRAM_VIDEO_URL
            )
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)
    send = (
        "**🤍 الـمـدة:** بـث مـبـاشـر (غـيـر مـحـدد)\n\nاضـغـط عـلـى الـزر بـالأسـفـل لـعـرض الـقـائـمـة كـامـلـة."
        if DUR == "Unknown"
        else "\nاضـغـط عـلـى الـزر بـالأسـفـل لـعـرض الـقـائـمـة كـامـلـة."
    )
    cap = f"""**{config.MUSIC_BOT_NAME} 🧚**

☔ **الاسـم:** {title}

🧚 **الـنـوع:** {typo}
💕 **طـلـب بـواسـطـة:** {user}
{send}"""
    upl = (
        queue_markup(_, DUR, cplay, videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            cplay,
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True

    med = InputMediaPhoto(media=IMAGE, caption=cap)
    mystic = await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if not await is_active_chat(chat_id):
                    break
                if basic[videoid]:
                    if await is_music_playing(chat_id):
                        try:
                            buttons = queue_markup(
                                _,
                                DUR,
                                cplay,
                                videoid,
                                seconds_to_min(db[chat_id][0]["played"]),
                                db[chat_id][0]["dur"],
                            )
                            await mystic.edit_reply_markup(reply_markup=buttons)
                        except FloodWait:
                            pass
                else:
                    break
        except Exception:
            return
