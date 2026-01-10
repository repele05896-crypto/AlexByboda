# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""


from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType, ChatMemberStatus
from config import SUPPORT_GROUP, adminlist
from strings import get_string
from AlexaMusic import app
from AlexaMusic.misc import SUDOERS
from AlexaMusic.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
)

from ..formatters import int_to_alpha


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        if await is_maintenance() is False and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                text=f"🧚 عذراً، {app.mention} يمر حالياً بعملية صيانة دورية لضمان أفضل أداء. يرجى زيارة <a href={SUPPORT_GROUP}>مجموعة الدعم الفني</a> لمتابعة آخر التحديثات ومعرفة موعد العودة.",
                disable_web_page_preview=True,
            )

        try:
            await message.delete()
        except Exception:
            pass

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except Exception:
            _ = get_string("en")
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="كيفية معالجة هذا الأمر ؟",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                await app.get_chat(chat_id)
            except Exception:
                return await message.reply_text(_["cplay_4"])
        else:
            chat_id = message.chat.id
        if not await is_active_chat(chat_id):
            return await message.reply_text(_["general_6"])
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_18"])
            if message.from_user.id not in admins:
                return await message.reply_text(_["admin_19"])
        return await mystic(client, message, _, chat_id)

    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        if await is_maintenance() is False and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                text=f"🧚 عذراً، {app.mention} يمر حالياً بعملية صيانة دورية لضمان أفضل أداء. يرجى زيارة <a href={SUPPORT_GROUP}>مجموعة الدعم الفني</a> لمتابعة آخر التحديثات ومعرفة موعد العودة.",
                disable_web_page_preview=True,
            )

        try:
            await message.delete()
        except Exception:
            pass

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except Exception:
            _ = get_string("en")
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="كيفية معالجة هذا الأمر ؟",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)
        if message.from_user.id not in SUDOERS:
            try:
                member = await app.get_chat_member(
                    message.chat.id, message.from_user.id
                )
                if (
                    member.status != ChatMemberStatus.ADMINISTRATOR
                    and not member.privileges.can_manage_video_chats
                ):
                    return await message.reply(_["general_5"])
            except Exception as e:
                return await message.reply(f"لقد حدث خطأ غير متوقع أثناء معالجة الطلب: {str(e)}")
        return await mystic(client, message, _)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if (
            await is_maintenance() is False
            and CallbackQuery.from_user.id not in SUDOERS
        ):
            return await CallbackQuery.answer(
                f"🧚 عذراً، {app.mention} يمر حالياً بعملية صيانة دورية لضمان أفضل أداء. يرجى زيارة مجموعة الدعم الفني لمتابعة آخر التحديثات.",
                show_alert=True,
            )
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            _ = get_string(language)
        except Exception:
            _ = get_string("en")
        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery, _)
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                a = await app.get_chat_member(
                    CallbackQuery.message.chat.id,
                    CallbackQuery.from_user.id,
                )
                if a.status != ChatMemberStatus.ADMINISTRATOR:
                    if not a.privileges.can_manage_video_chats:
                        if CallbackQuery.from_user.id not in SUDOERS:
                            token = await int_to_alpha(CallbackQuery.from_user.id)
                            _check = await get_authuser_names(
                                CallbackQuery.from_user.id
                            )
                            if token not in _check:
                                return await CallbackQuery.answer(
                                    _["general_5"],
                                    show_alert=True,
                                )
                    elif a is None:
                        return await CallbackQuery.answer(
                            "عذراً، يبدو أنك لست عضواً مسجلاً في هذه المجموعة."
                        )
            except Exception as e:
                return await CallbackQuery.answer(f"لقد حدث خطأ غير متوقع: {str(e)}")
        return await mystic(client, CallbackQuery, _)

    return wrapper
