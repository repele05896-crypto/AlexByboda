# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


import sys

from pyrogram import Client
import config
from ..logging import LOGGER
from pyrogram.enums import ChatMemberStatus


class AlexaBot(Client):
    def __init__(self):
        super().__init__(
            "MusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            max_concurrent_transmissions=5,
        )
        LOGGER(__name__).info("جاري تهيئة ملفات البوت وبدء التشغيل...")

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.mention = get_me.mention
        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                "🧚 أهلاً بك سيدي المطور، لقد تم تشغيل البوت الخاص بك بنجاح وهو الآن يعمل بكامل طاقته في السيرفر. نحن الآن في انتظار انضمام الحساب المساعد للبدء في تشغيل الموسيقى."
            )
        except Exception:
            LOGGER(__name__).error(
                "🥀 عذراً، فشل البوت في الوصول إلى مجموعة السجل الخاصة بك. يرجى التأكد من أنك قمت بإضافة البوت إلى القناة أو المجموعة المخصصة للسجل، وتأكد أيضاً من رفعه مشرفاً (Admin) بصلاحيات كاملة."
            )
            sys.exit()
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("🥀 عذراً، يرجى رفع البوت مشرفاً (Admin) في مجموعة السجل (Logger Group) حتى يتمكن من إرسال التقارير والعمل بشكل صحيح.")
            sys.exit()
        if get_me.last_name:
            self.name = f"{get_me.first_name} {get_me.last_name}"
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"تم بدء تشغيل البوت بنجاح تحت اسم: {self.name}")
