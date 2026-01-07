# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

from pyrogram.enums import ParseMode

from config import LOG_GROUP_ID
from AlexaMusic.utils.database import is_on_off
from AlexaMusic import app


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>سـجـل تـشـغـيـل {app.mention}</b>

<b>آيـدي الـمـجـمـوعـة :</b> <code>{message.chat.id}</code>
<b>اسـم الـمـجـمـوعـة :</b> {message.chat.title}
<b>يـوزر الـمـجـمـوعـة :</b> @{message.chat.username}

<b>آيـدي الـمـشـغـل :</b> <code>{message.from_user.id}</code>
<b>اسـم الـمـشـغـل :</b> {message.from_user.mention}
<b>يـوزر الـمـشـغـل :</b> @{message.from_user.username}

<b>الـمـطـلـوب :</b> {message.text.split(None, 1)[1]}
<b>نـوع الـتـشـغـيـل :</b> {streamtype}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception:
                pass
        return
