# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

from strings import get_string
from AlexaMusic.misc import SUDOERS
from AlexaMusic.utils.database import get_lang, is_commanddelete_on, is_maintenance

# دالة ذكية للتعامل مع اللغات
async def smart_language_check(chat_id):
    try:
        lang = await get_lang(chat_id)
        
        # الحالة 1: مستخدم جديد ليس له لغة -> نعطيه العربية
        if not lang:
            return "en"
            
        # الحالة 2: مستخدم لغته "en" (وهي الافتراضية القديمة التي نريد تغييرها) -> نحولها عربية
        # ملاحظة: إذا كنت تريد السماح بالإنجليزية لمن يختارها يدوياً، احذف السطرين التاليين
        if lang == "en":
            return "en"
            
        # الحالة 3: أي لغة أخرى محفوظة (غير الإنجليزية والفراغ) -> نتركها كما هي
        return lang
    except:
        return "en"

def language(mystic):
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                "🧚 عذراً، البوت في وضع الصيانة حالياً لإجراء التحديثات اللازمة. يرجى المحاولة في وقت لاحق."
            )
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except Exception:
                pass
        
        lang_code = await smart_language_check(message.chat.id)
        language = get_string(lang_code)
        return await mystic(_, message, language)

    return wrapper


def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        if (
            await is_maintenance() is False
            and CallbackQuery.from_user.id not in SUDOERS
        ):
            return await CallbackQuery.answer(
                "🧚 عذراً، البوت في وضع الصيانة حالياً لإجراء التحديثات اللازمة. يرجى المحاولة في وقت لاحق.",
                show_alert=True,
            )
        
        lang_code = await smart_language_check(CallbackQuery.message.chat.id)
        language = get_string(lang_code)
        return await mystic(_, CallbackQuery, language)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        lang_code = await smart_language_check(message.chat.id)
        language = get_string(lang_code)
        return await mystic(_, message, language)

    return wrapper
