# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

from pyrogram import filters
from pyrogram.types import Message

import config
from strings import get_command
from AlexaMusic import app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.utils.database import add_off, add_on
from AlexaMusic.utils.decorators.language import language

# Commands
VIDEOMODE_COMMAND = get_command("VIDEOMODE_COMMAND")

# إضافة الأمر العربي "وضع الفيديو"
if isinstance(VIDEOMODE_COMMAND, str):
    VIDEOMODE_COMMAND = [VIDEOMODE_COMMAND, "وضع الفيديو"]
elif isinstance(VIDEOMODE_COMMAND, list):
    VIDEOMODE_COMMAND.append("وضع الفيديو")


@app.on_message(filters.command(VIDEOMODE_COMMAND) & SUDOERS)
@language
async def videoloaymode(client, message: Message, _):
    usage = _["vidmode_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    
    # تم التعديل ليقبل "download" أو "تحميل" أو "تنزيل"
    if state in ["download", "تحميل", "تنزيل"]:
        await add_on(config.YTDOWNLOADER)
        await message.reply_text(_["vidmode_2"])
    
    # تم التعديل ليقبل "m3u8" أو "بث"
    elif state in ["m3u8", "بث"]:
        await add_off(config.YTDOWNLOADER)
        await message.reply_text(_["vidmode_3"])
    
    else:
        await message.reply_text(usage)
