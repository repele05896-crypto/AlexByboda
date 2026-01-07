# Copyright (C) 2025 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

"""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2021 ~ Present Team Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_GROUP, SUPPORT_CHANNEL
import math

# --- استيراد الدوال من ملف التنسيق ---
# تأكد أن اسم المجلد والملف صحيحين في مشروعك
# غالباً يكون المسار: AlexaMusic.utils.formatters
try:
    from AlexaMusic.utils.formatters import seconds_to_min
except ImportError:
    # دالة احتياطية في حال فشل الاستيراد لتجنب توقف البوت
    def seconds_to_min(seconds):
        if seconds is not None:
            seconds = int(seconds)
            d, h, m, s = (
                seconds // (3600 * 24),
                seconds // 3600 % 24,
                seconds % 3600 // 60,
                seconds % 3600 % 60,
            )
            if d > 0:
                return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
            elif h > 0:
                return "{:02d}:{:02d}:{:02d}".format(h, m, s)
            elif m > 0:
                return "{:02d}:{:02d}".format(m, s)
            elif s > 0:
                return "00:{:02d}".format(s)
        return "-"


## Helper Function to Calculate Bar
def get_progress_bar(played, dur):
    try:
        # Convert "MM:SS" or "HH:MM:SS" to seconds
        def to_sec(t):
            parts = t.split(':')
            if len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            return 0

        played_sec = to_sec(played)
        dur_sec = to_sec(dur)

        if dur_sec == 0:
            percentage = 0
        else:
            percentage = (played_sec / dur_sec) * 100
    except:
        percentage = 0

    umm = math.floor(percentage)

    if 0 < umm <= 10:
        bar = "❥—————————"
    elif 10 < umm < 20:
        bar = "—❥————————"
    elif 20 <= umm < 30:
        bar = "——❥———————"
    elif 30 <= umm < 40:
        bar = "———❥——————"
    elif 40 <= umm < 50:
        bar = "————❥—————"
    elif 50 <= umm < 60:
        bar = "—————❥————"
    elif 60 <= umm < 70:
        bar = "——————❥———"
    elif 70 <= umm < 80:
        bar = "———————❥——"
    elif 80 <= umm < 95:
        bar = "————————❥—"
    else:
        bar = "—————————❥"
    
    return bar


## After Edits with Timer Bar

def stream_markup_timer(_, videoid, chat_id, played, dur):
    bar = get_progress_bar(played, dur)
    return [
        [
            InlineKeyboardButton(
                text=f"{played} •{bar}• {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_2"],
                callback_data=f"add_playlist {videoid}",
            ),
            InlineKeyboardButton(text="الـمـطـور", url="https://t.me/S_G0C7"),
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(text="الـدعـم", url=SUPPORT_GROUP),
        ],
        [InlineKeyboardButton(text="الـتـحـديـثـات", url=SUPPORT_CHANNEL)],
    ]


def telegram_markup_timer(_, videoid, chat_id, played, dur):
    bar = get_progress_bar(played, dur)
    return [
        [
            InlineKeyboardButton(
                text=f"{played} •{bar}• {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_2"],
                callback_data=f"add_playlist {videoid}",
            ),
            InlineKeyboardButton(text="الـمـطـور", url="https://t.me/S_G0C7"),
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
            InlineKeyboardButton(text="الـدعـم", url=SUPPORT_GROUP),
        ],
    ]


## Inline without Timer Bar


def stream_markup(_, videoid, chat_id):
    return [
        [
            InlineKeyboardButton(
                text=_["PL_B_2"],
                callback_data=f"add_playlist {videoid}",
            ),
            InlineKeyboardButton(text="الـمـطـور", url="https://t.me/S_G0C7"),
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
            InlineKeyboardButton(text="الـدعـم", url=SUPPORT_GROUP),
        ],
    ]


def telegram_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
        ],
    ]


## By Anon
close_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="إغـلاق", callback_data="close")]]
)

## Search Query Inline


def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"{SUPPORT_GROUP}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


## Live Stream Markup


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"{SUPPORT_GROUP}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


## Slider Query Markup


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]


## Cpanel Markup


def panel_markup_1(_, videoid, chat_id):
    return [
        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_2"],
                callback_data=f"add_playlist {videoid}",
            ),
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"{SUPPORT_GROUP}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⇆ خـلـط ⇆",
                callback_data=f"ADMIN Shuffle|{chat_id}",
            ),
            InlineKeyboardButton(
                text="↻ تـكـرار ↻", callback_data=f"ADMIN Loop|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="《 10 ثـوانـي",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="10 ثـوانـي 》",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="《 30 ثـانـيـة",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
            InlineKeyboardButton(
                text="30 ثـانـيـة 》",
                callback_data=f"ADMIN 4|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="↻ رجـوع ↻",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
        ],
    ]


## Queue Markup Anon


def queue_markup(_, videoid, chat_id):
    return [
        [
            InlineKeyboardButton(
                text="▷",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="☆", callback_data=f"add_playlist {videoid}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [InlineKeyboardButton(text="إغـلاق", callback_data=f"ADMIN CloseA|{chat_id}")],
    ]
