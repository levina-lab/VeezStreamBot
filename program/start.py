from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@ᴄʟɪᴇɴᴛ.ᴏɴ_ᴍᴇssᴀɢᴇ(ᴄᴏᴍᴍᴀɴᴅ("sᴛᴀʀᴛ") & ғɪʟᴛᴇʀs.ᴘʀɪᴠᴀᴛᴇ & ~ғɪʟᴛᴇʀs.ɢʀᴏᴜᴘ & ~ғɪʟᴛᴇʀs.ᴇᴅɪᴛᴇᴅ)
ᴀsʏɴᴄ ᴅᴇғ sᴛᴀʀᴛ_(ᴄʟɪᴇɴᴛ: ᴄʟɪᴇɴᴛ, ᴍᴇssᴀɢᴇ: ᴍᴇssᴀɢᴇ):
    ᴀᴡᴀɪᴛ ᴍᴇssᴀɢᴇ.ʀᴇᴘʟʏ_sᴛɪᴄᴋᴇʀ("ᴄᴀᴀᴄᴀɢǫᴀᴀxᴋʙᴀᴀɪᴄ_ᴍʜ𝟷ᴊᴜʀʟ_s𝟺ᴋɢᴋᴀ𝟻ʜɪᴅᴋ_ʀʀʟ𝟶ɢʏᴡᴀᴀɪᴇᴄɢᴀᴄᴢ𝟿ʏʀᴜxɴᴜᴄʜᴘ𝟻ᴋɢᴊғɪᴡǫ")
    ᴀᴡᴀɪᴛ ᴍᴇssᴀɢᴇ.ʀᴇᴘʟʏ_ᴘʜᴏᴛᴏ(
        ᴘʜᴏᴛᴏ=ғ"ʜᴛᴛᴘs://ᴛᴇ.ʟᴇɢʀᴀ.ᴘʜ/ғɪʟᴇ/ғғʙʙ𝟶𝟿𝟼ᴅ𝟷𝟶ᴅᴅ𝟹𝟼ᴀᴅ𝟺𝟻𝟹𝟹𝟽.ᴊᴘɢ",
        ᴄᴀᴘᴛɪᴏɴ=ғ"""**━━━━━━━━━━━━ 🌺🌻🌹🌷━━━━━━━━━━
━━━━━━━━━━━━━ 🌺🌻🌹🌷━━━━━━━━━━━━━
😊ʜɪ ɪᴀᴍ ᴛᴇʟᴇɢʀᴀᴍ ᴠᴏɪᴄᴇ ᴍᴜsɪᴄ ʙᴏᴛ... ᴅᴇᴘʟᴏʏ ʙʏ : @sᴀɴᴛʜᴜ_ᴍᴜsɪᴄ_ʙᴏᴛ
┏━━━━━━━━━━━━━━━━━┓ 🌺🌻🌹🌷🌺🌻🌹
┣» ᴏᴘ ᴍᴜꜱɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ. 
┣» ʜɪɢʜ ǫᴜᴀʟɪᴛʏ  ᴍᴜꜱɪᴄ.
┣» ᴀᴅᴠᴀɴᴄᴇᴅ ꜰᴇᴀᴛᴜʀᴇꜱ.
┣» ꜱᴜᴘᴇʀꜰᴀꜱᴛ ꜱᴘᴇᴇᴅ. 
┣» [𝐃𝐄𝐏𝐋𝐎𝐘 𝐁𝐘 ❤️](ʜᴛᴛᴘs://ᴛ.ᴍᴇ/sᴀɴᴛʜᴜ_ᴍᴜsɪᴄ_ʙᴏᴛ)
┗━━━━━━━━━━━━━━━━━┛
[𝐎𝐖𝐍𝐄𝐑 ❤️](ʜᴛᴛᴘs://ᴛ.ᴍᴇ/sᴀɴᴛʜᴜ_ᴍᴜsɪᴄ_ʙᴏᴛ)
𝐈𝐟 𝐘𝐨𝐮 𝐇𝐚𝐯𝐞 𝐀𝐧𝐲 𝐐𝐮𝐞𝐬𝐭𝐢𝐨𝐧𝐬 𝐀𝐧𝐝 𝐇𝐞𝐥𝐩 𝐓𝐡𝐞𝐧 𝐃𝐦 𝐌𝐲 𝐁𝐨𝐬𝐬 = [𝐒𝐀𝐍𝐓𝐇𝐔❤️](ʜᴛᴛᴘs://ᴛ.ᴍᴇ/sᴀɴᴛʜᴜ_ᴍᴜsɪᴄ_ʙᴏᴛ)
━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💞 ɴᴀɴᴜ ᴀᴅᴅ ᴄʜᴇsᴜᴋᴏɴᴅɪ 🥺",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Basic Guide", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("🥰 Commands", callback_data="cbcmds"),
                    InlineKeyboardButton("❤️ Donate", url=f"https://t.me/santhu_music_bot"),
                ],
                [
                    InlineKeyboardButton(
                        "🙂 ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/santhuvc"
                    ),
                    InlineKeyboardButton(
                        "😁 sᴀɴᴛʜᴜ Channel", url=f"https://t.me/santhubotupadates"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "😊 Source Code", url="https://t.me/santhuvc"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(c: Client, message: Message):
    chat_id = message.chat.id
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/santhuvc"),
                InlineKeyboardButton(
                    "😇 sᴀɴᴛʜᴜ ɢʀᴏᴜᴘ", url=f"https://t.me/santhuvc"
                ),
            ]
        ]
    )

    alive = f"**Hello {message.from_user.mention()}, i'm {BOT_NAME}**\n\n🧑🏼‍💻 My Master: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n👾 Bot Version: `v{__version__}`\n🔥 Pyrogram Version: `{pyrover}`\n🐍 Python Version: `{__python_version__}`\n✨ PyTgCalls Version: `{pytover.__version__}`\n🆙 Uptime Status: `{uptime}`\n\n❤ **Thanks for Adding me here, for playing video & music on your Group's video chat**"

    await c.send_photo(
        chat_id,
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ ɴᴀɴᴜ ᴀᴅᴅ ᴄʜᴇsɪɴᴅʜᴜᴋᴜ ᴛʜᴀɴᴋs**Group** !\n\n"
                "Appoint me as administrator in the **Group**, otherwise I will not be able to work properly, and don't forget to type `/userbotjoin` for invite the assistant.\n\n"
                "Once done, then type `/reload`",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 sᴀɴᴛʜᴜ", url=f"https://t.me/santhuvc"),
                            InlineKeyboardButton("💭 ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/santhuvc")
                        ],
                        [
                            InlineKeyboardButton("👤 sᴀɴᴛʜᴜ ᴀssɪsᴛᴀɴᴛ", url=f"https://t.me/santhu_music_bot")
                        ]
                    ]
                )
            )
