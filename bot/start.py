# Copyright (C) 2021 By VeezMusicProject

from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import Veez
from helpers.decorators import sudo_users_only
from helpers.filters import command

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{Veez.BOT_USERNAME}"]))
async def start(_, m: Message):
    if m.chat.type == "private":
        await m.reply_text(
            f"✨ **Hello there, I am a telegram group video streaming bot.**\n\n💭 **I was created to stream videos in group "
            f"video chats easily.**\n\n❔ **To find out how to use me, please press the help button below** 👇🏻",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "➕ Add me to your Group ➕", url=f"https://t.me/{Veez.BOT_USERNAME}?startgroup=true")
                ], [
                    InlineKeyboardButton(
                        "❔ HOW TO USE THIS BOT", callback_data="cbguide")
                ], [
                    InlineKeyboardButton(
                        "🌐 Terms & Condition", callback_data="cbinfo")
                ], [
                    InlineKeyboardButton(
                        "💬 Group", url="https://t.me/trtechguide"),
                    InlineKeyboardButton(
                        "📣 Channel", url="https://t.me/SLBotsOfficial")
                ], [
                    InlineKeyboardButton(
                        "👩🏻‍💻 Developer", url="https://t.me/TharukRenuja")
                ], [
                    InlineKeyboardButton(
                        "📚 All Command List", callback_data="cblist")
                ]]
            ))
    else:
        await m.reply_text("**✨ bot is online now ✨**",
                           reply_markup=InlineKeyboardMarkup(
                               [[
                                   InlineKeyboardButton(
                                       "❔ HOW TO USE THIS BOT", callback_data="cbguide")
                               ], [
                                   InlineKeyboardButton(
                                       "🌐 Search Youtube", switch_inline_query='')
                               ], [
                                   InlineKeyboardButton(
                                       "📚 Command List", callback_data="cblist")
                               ]]
                           )
                           )


@Client.on_message(command(["alive", f"alive@{Veez.BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def alive(_, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"""✅ **bot is running**\n<b>💠 **uptime:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ Group", url=f"https://t.me/trtechguide"
                    ),
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/SLBotsOfficial"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{Veez.BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(_, m: Message):
    sturt = time()
    m_reply = await m.reply_text("pinging...")
    delta_ping = time() - sturt
    await m_reply.edit_text(
        "🏓 `PONG!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{Veez.BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(_, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 bot status 🤖\n\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
